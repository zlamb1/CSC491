from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
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

def get_historical_data(symbol_or_symbols):
    stock_client = StockHistoricalDataClient("PKD3ZQC5RNBSD4DIQVETFAI3SD", "GH2WhT5oPtcMTQzjZMCpao3TGT5tG55xghNQ4W3aGkv9")
    
    if not isinstance(symbol_or_symbols, list):
        symbol_or_symbols = [symbol_or_symbols]

    formatted_request = StockBarsRequest(
        symbol_or_symbols=symbol_or_symbols,
        start=datetime(2025, 4,18),
        end=datetime(2026,2,12),
        timeframe=TimeFrame.Minute
    )

    response = stock_client.get_stock_bars(formatted_request)

    df = response.df
    df.dropna(inplace=True)
    df = df[df.volume != 0]

    return df

def scrape_stock_analysis(limit=1000):
    base_url = "https://stockanalysis.com/list/biggest-companies/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    all_data = []

    # The site typically shows 500 per page, so we check page 1 and 2
    for page in range(1, 3):
        url = f"{base_url}?p={page}" if page > 1 else base_url
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'main-table'})
        if not table:
            break

        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 6:
                # Mapping based on website structure: Ticker, Name, Market Cap, Price, Change, Sector, Industry
                ticker = cols[1].text.strip()
                name = cols[2].text.strip()
                mcap = cols[3].text.strip()
                sector = cols[5].text.strip()
                industry = cols[6].text.strip()
                all_data.append([ticker, name, mcap, sector, industry])

        if len(all_data) >= limit:
            break

    df = pd.DataFrame(all_data[:limit], columns=['Ticker', 'Name', 'Market Cap', 'Sector', 'Industry'])
    return df