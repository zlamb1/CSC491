from csc491 import fetch, graph, transform

stock_ticker = input('Enter Stock Ticker: ')
df = fetch.get_historical_data(stock_ticker)
db = transform.gen_dollar_bars(df)
graph.log_returns([df, db], ['close', 'price'])