import os

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

cachedir = '.cache'

def get_path(symbol):
    return f"{cachedir}/{symbol}.parquet"

def write_stock(symbol, df):
    try:
        os.mkdir(cachedir)
    except:
        pass

    table = pa.Table.from_pandas(df)
    pq.write_table(table, get_path(symbol))

def read_stock(symbol):
    parquetpath = get_path(symbol)
    if not os.path.isfile(parquetpath):
        return None
    return pd.read_parquet(parquetpath)

if __name__ == '__main__':
    import csc491
    df, filtered = csc491.fetch.find_top_1000_stocks()
    cache_stocks(df, filtered)