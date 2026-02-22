from alpaca.data import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from datetime import datetime
from db import market_caps as _market_caps

import csc491
import json

outfile = 'db/top_1000.json'

def get():
    with open(outfile, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    symbols = csc491.api.get_ticker_symbols()

    market_caps = _market_caps.get()

    def sortby(symbol):
        if not symbol in market_caps:
            print(f'Warning: market cap for {symbol} not found')
            return 0
        return market_caps[symbol]

    symbols = sorted(symbols, key=sortby, reverse=True)
    top_1000 = []
    min_market_cap = 1_300_000

    for symbol in symbols:
        df = csc491.api.get_ticker_data(symbol, timeframe=csc491.api.TimeFrame.Month)
        if df is None:
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