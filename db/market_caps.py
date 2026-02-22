from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

import csc491
import json
import pandas as pd
import time
import yahooquery as yq

env = csc491.env.load()

api_key = env.get('ALPACA_API_KEY')
if api_key is None:
    raise RuntimeError('Supply ALPACA_API_KEY in .env')

secret_key = env.get('ALPACA_SECRET_KEY')
if secret_key is None:
    raise RuntimeError('Supply ALPACA_SECRET_KEY in .env')

trade_client = TradingClient(api_key, secret_key)

assets = trade_client.get_all_assets(GetAssetsRequest(status="active", asset_class="us_equity"))
symbols = []
for asset in assets:
    symbols.append(asset.symbol)

batch = 500
outfile = 'db/market_caps.json'

market_caps = {}

try:
    with open(outfile, 'r') as f:
        market_caps = json.load(f)
except FileNotFoundError:
    pass

for i in range(0, len(symbols), batch):
    print(f'{i} / {len(symbols)}')

    current = symbols[i:i + batch]
    accumulator = []

    for symbol in current:
        if not symbol in market_caps:
            accumulator.append(symbol)

    if len(accumulator) == 0:
        continue

    current = accumulator
    ticker = yq.Ticker(current, asynchronous=True)
    price = ticker.price
    done = False

    for symbol in current:
        market_cap = 0

        data = price.get(symbol)
        if isinstance(data, dict):
            market_cap = data.get('marketCap', 0)
        else:
            if data == 'Invalid Crumb':
                done = True
                break
            print(f'Skipping {symbol}: {data}')

        market_caps[symbol] = market_cap
    
    if done:
        break

with open(outfile, 'w') as f:
    json.dump(market_caps, f, indent=4)