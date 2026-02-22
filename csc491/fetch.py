from alpaca.data import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest, StockLatestQuoteRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

from bs4 import BeautifulSoup
from datetime import datetime

import csc491
import pandas as pd
import requests

env = csc491.env.load()

api_key = env.get('ALPACA_API_KEY')
if api_key is None:
    raise RuntimeError('Supply ALPACA_API_KEY in .env')

secret_key = env.get('ALPACA_SECRET_KEY')
if secret_key is None:
    raise RuntimeError('Supply ALPACA_SECRET_KEY in .env')

stock_client = StockHistoricalDataClient(api_key, secret_key)
trade_client = TradingClient(api_key, secret_key)

def get_historical_data(symbol_or_symbols):
    formatted_request = StockBarsRequest(
        symbol_or_symbols=symbol_or_symbols,
        start=datetime(2022, 1, 1),
        end=datetime.now(),
        timeframe=TimeFrame.Minute
    )

    response = stock_client.get_stock_bars(formatted_request)

    df = response.df
    if df.empty:
        return None

    df.dropna(inplace=True)
    df = df[df.volume != 0]

    return df

def find_top_1000_stocks():
    assets = trade_client.get_all_assets(GetAssetsRequest(status="active", asset_class="us_equity"))
    symbols = []
    for a in assets:
        symbols.append(a.symbol)
    # not_found = []
    # step = 1000

    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        market_cap = ticker.fast_info['market_cap']
        print(f'{symbol}: {market_cap}')

    #for symbol in symbols:
    #    df = csc491.cache.read_stock(symbol)
    #    if df is None:
    #        not_found.append(symbol)
#
    #for i in range(0, len(not_found), step):
    #    cur = not_found[i:i+1000]
    #    df = get_historical_data(cur)
    #    level_values = df.index.get_level_values(0)
    #    for symbol in cur:
    #        if not symbol in level_values:
    #            #print(f'Warning: no stock ticker data found for {symbol}')
    #            csc491.cache.write_stock(symbol, pd.DataFrame())
    #            continue
    #        csc491.cache.write_stock(symbol, df.loc[symbol])

    # df['dv'] = df['close'] * df['volume']
    # Sort symbols by dollar volume and take top 1000.
    # return df, df.groupby('symbol')['dv'].sum().nlargest(1000)