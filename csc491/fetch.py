from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from datetime import datetime
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

stock_client = StockHistoricalDataClient("#", "#")

def get_historical_data(stock_ticker):
    formatted_request = StockBarsRequest(
        symbol_or_symbols=[stock_ticker],
        start=datetime(2025, 4,18),
        end=datetime(2026,2,12),
        timeframe=TimeFrame.Minute
    )

    response = stock_client.get_stock_bars(formatted_request)
    df = response.df

    df.dropna(inplace=True)
    df = df[df.volume != 0]

    return df