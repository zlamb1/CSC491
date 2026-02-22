from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

import csc491
import json
import pandas as pd
import time
import yahooquery as yq

outfile = 'db/market_caps.json'

def get():
    with open(outfile, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    batch = 500
    market_caps = {}

    try:
        with open(outfile, 'r') as f:
            market_caps = json.load(f)
    except FileNotFoundError:
        pass

    symbols = csc491.api.get_ticker_symbols()

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