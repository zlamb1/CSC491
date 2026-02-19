import pandas as pd

from contextlib import closing

def gen_dollar_bars(df):
    close_price = 0.00
    stocks = 0
    closing_prices = df[['close', 'volume']]
    rows = len(closing_prices)
    bars_index = 1
    bars = []
    current_dollars = 0.00
    index = 0

    threshold = 560000000 # Note: Placeholder until strategist number is determined.

    while index < rows:
        price = closing_prices['close']
        close_price = price.iloc[index]
        volume = closing_prices['volume']
        stocks = volume.iloc[index]
        current_dollars += close_price * stocks
        index += 1

        while current_dollars >= threshold:
            multi_index = (bars_index, df.index[index][1])
            bars.append((multi_index, close_price))
            bars_index += 1
            current_dollars -= threshold

    index, prices = zip(*bars)
    multi_index = pd.MultiIndex.from_tuples(index, names=['bar', 'timestamp'])
    dollar_bars = pd.DataFrame({ 'price':  prices }, index=multi_index)
    return dollar_bars