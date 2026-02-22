from alpaca.data import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from datetime import datetime

import csc491
import json

env = csc491.env.load()

api_key = env.get('ALPACA_API_KEY')
if api_key is None:
    raise RuntimeError('Supply ALPACA_API_KEY in .env')

secret_key = env.get('ALPACA_SECRET_KEY')
if secret_key is None:
    raise RuntimeError('Supply ALPACA_SECRET_KEY in .env')

stock_client = StockHistoricalDataClient(api_key, secret_key)
trade_client = TradingClient(api_key, secret_key)

assets = trade_client.get_all_assets(GetAssetsRequest(status="active", asset_class="us_equity"))
symbols = []
for asset in assets:
    if getattr(asset, 'asset_type', None) != 'stock' or not asset.tradable:
        continue

    symbols.append(asset.symbol)

infile = 'db/market_caps.json'
outfile = 'db/top_1000.json'

with open(infile, 'r') as f:
    market_caps = json.load(f)

def sortby(symbol):
    if not symbol in market_caps:
        print(f'Warning: market cap for {symbol} not found')
        return 0
    return market_caps[symbol]

symbols = sorted(symbols, key=sortby, reverse=True)
top_1000 = []
min_market_cap = 1_300_000

for symbol in symbols:
    now = datetime.now()

    formatted_request = StockBarsRequest(
        symbol_or_symbols=symbol,
        start=datetime(now.year, now.month, 1),
        end=now,
        timeframe=TimeFrame.Month
    )

    response = stock_client.get_stock_bars(formatted_request)

    df = response.df
    if df.empty:
        continue

    if market_caps.get(symbol, 0) < min_market_cap:
        print(f'Warning: {symbol} below minimum market cap')

    top_1000.append(symbol)
    print(len(top_1000))
    if len(top_1000) == 1000:
        break

if len(top_1000) < 1000:
    print('Warning: less than 1000 stocks were collated')

with open(outfile, 'w') as f:
    json.dump(top_1000, f, indent=4)