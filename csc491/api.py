from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame as AlpacaTimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

from csc491 import env
from datetime import datetime
from enum import StrEnum
from functools import cache

@cache
def _get_api_credentials():
    _env = env.load()

    api_key = _env.get('ALPACA_API_KEY')
    if api_key is None:
        raise RuntimeError('Supply ALPACA_API_KEY in .env')
    
    secret_key = _env.get('ALPACA_SECRET_KEY')
    if secret_key is None:
        raise RuntimeError('Supply ALPACA_SECRET_KEY in .env')

    return api_key, secret_key

@cache
def _get_stock_client():
    api_key, secret_key = _get_api_credentials()
    return StockHistoricalDataClient(api_key, secret_key)

@cache
def _get_trade_client():
    api_key, secret_key = _get_api_credentials()
    return TradingClient(api_key, secret_key)

class TimeFrame(StrEnum):
    Minute = 'minute'
    Hour = 'hour'
    Day = 'day'
    Week = 'week'
    Month = 'month'

def get_ticker_symbols():
    trade_client = _get_trade_client()
    assets = trade_client.get_all_assets(GetAssetsRequest(status="active", asset_class="us_equity"))
    return [asset.symbol for asset in assets]

def get_ticker_data(symbol_or_symbols, start=None, end=None, timeframe=TimeFrame.Minute):     
    if start is None:
        start = datetime.now()
        start = start.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    if end is None:
        end = datetime.now()

    if timeframe == TimeFrame.Minute:
        timeframe = AlpacaTimeFrame.Minute
    elif timeframe == TimeFrame.Hour:
        timeframe = AlpacaTimeFrame.Hour
    elif timeframe == TimeFrame.Day:
        timeframe = AlpacaTimeFrame.Day
    elif timeframe == TimeFrame.Week:
        timeframe = AlpacaTimeFrame.Week
    elif timeframe == TimeFrame.Month:
        timeframe = AlpacaTimeFrame.Month
    else:
        raise ValueError(f'Invalid Time Frame {timeframe} (use the TimeFrame enum).')

    stock_client = _get_stock_client()

    formatted_request = StockBarsRequest(
        symbol_or_symbols=symbol_or_symbols,
        start=start,
        end=end,
        timeframe=timeframe
    )

    response = stock_client.get_stock_bars(formatted_request)

    df = response.df
    if df.empty:
        return None

    df.dropna(inplace=True)
    df = df[df.volume != 0]

    return df