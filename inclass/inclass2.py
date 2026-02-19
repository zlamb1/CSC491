from csc491 import fetch, graph, transform

stock_ticker = input('Enter Stock Ticker: ')
df = fetch.get_historical_data(stock_ticker)
graph.bar_count([df, df], titles=['Time Bars', 'Dollar Bars'])