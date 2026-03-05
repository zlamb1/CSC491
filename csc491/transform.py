import numpy as np
import pandas as pd

from contextlib import closing

def get_thresholds(df, timestamps, bars_per_day=50, window=30):
    ddv = df['close'] * df['volume']
    ddv = ddv.groupby(pd.Grouper(level=1, freq='D')).sum()
    # Calculate the rolling daily dollar volume average and backfill.
    raddv = ddv.shift(1).rolling(window=window).mean().replace(0, np.nan).bfill()
    return (timestamps.normalize().map(raddv) / bars_per_day).values

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

    thresholds = get_thresholds(df, timestamps)

    while i < rows:
        timestamp = timestamps[i]
        close = closes[i]
        volume = volumes[i]
        current_dollars += close * volume
        threshold = thresholds[i]

        progress = (i/rows)*100

        while current_dollars >= threshold:
            multi_index = (bar, timestamp)
            bars.append((multi_index, close))
            bar += 1
            current_dollars -= threshold

        i += 1

    index, closes = zip(*bars)
    multi_index = pd.MultiIndex.from_tuples(index, names=['bar', 'timestamp'])
    dollar_bars = pd.DataFrame({ 'close':  closes }, index=multi_index)
    return dollar_bars