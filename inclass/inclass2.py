from csc491 import fetch, graph, transform

stock_ticker = input('Enter Stock Ticker: ')
df = fetch.get_historical_data(stock_ticker)
db = transform.gen_dollar_bars(df)
jb_stat, p_value = graph.jarque_bera(df, 'close')
print(f'time bars jb_stat : {jb_stat}, p_value : {p_value}')
jb_stat, p_value = graph.jarque_bera(db, 'price')
print(f'dollar bars jb_stat : {jb_stat}, p_value : {p_value}')
graph.bar_count([df, db], titles=['Time Bars', 'Dollar Bars'])