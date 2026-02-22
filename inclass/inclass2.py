from csc491 import api, graph, transform

stock_ticker = input('Enter Stock Ticker: ')
df = api.get_ticker_data(stock_ticker, start=api.datetime(2022, 1, 1))
print('Transforming...')
db = transform.gen_dollar_bars(df)
print('Jarque-Bera...')
jb_stat, p_value = graph.jarque_bera(df, 'close')
print(f'time bars jb_stat : {jb_stat}, p_value : {p_value}')
jb_stat, p_value = graph.jarque_bera(db, 'price')
print(f'dollar bars jb_stat : {jb_stat}, p_value : {p_value}')
graph.bar_count(stock_ticker, [df, db], titles=['Time Bars', 'Dollar Bars'])