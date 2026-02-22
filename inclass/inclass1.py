from csc491 import api, graph, transform

stock_ticker = input('Enter Stock Ticker: ')
df = api.get_ticker_data(stock_ticker)
db = transform.gen_dollar_bars(df)
graph.log_returns(stock_ticker, [df, db], ['close', 'price'])