import pandas as pd

from contextlib import closing

def gen_dollar_bars(df):
    close_price = 0.00
    stocks = 0
    timestamps = df.index.get_level_values(1)
    closes = df['close'].values
    volumes = df['volume'].values
    rows = len(df)
    bar = 1
    bars = []
    current_dollars = 0.00
    i = 0

    threshold = 2500000000 # Note: Placeholder until strategist number is determined.

    while i < rows:
        timestamp = timestamps[i]
        close = closes[i]
        volume = volumes[i]
        current_dollars += close * volume
        
        while current_dollars >= threshold:
            multi_index = (bar, timestamp)
            bars.append((multi_index, close))
            bar += 1
            current_dollars -= threshold

        i += 1

    index, prices = zip(*bars)
    multi_index = pd.MultiIndex.from_tuples(index, names=['bar', 'timestamp'])
    dollar_bars = pd.DataFrame({ 'price':  prices }, index=multi_index)
    return dollar_bars