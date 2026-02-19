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
        start=datetime(2025, 4,18),
        end=datetime(2026,2,12),
        timeframe=TimeFrame.Week
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
    not_found = []
    for i in range(len(symbols[0:1000])):
        symbol = symbols[i]
        df = csc491.cache.read_stock(symbol)
        if df is None:
            not_found.append(symbol)
        else:
            print(df)
    if len(not_found) > 0:
        df = get_historical_data(not_found)
        for symbol in not_found:
            if not symbol in df.index.get_level_values(0):
                print(f'Warning: no stock ticker data found for {symbol}')
                continue
            csc491.cache.write_stock(symbol, df.loc[symbol])
    # df['dv'] = df['close'] * df['volume']
    # Sort symbols by dollar volume and take top 1000.
    # return df, df.groupby('symbol')['dv'].sum().nlargest(1000)