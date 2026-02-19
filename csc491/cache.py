from csc491 import fetch

import os

import pyarrow as pa
import pyarrow.parquet as pq

if __name__ == '__main__':
    df, filtered = fetch.find_top_1000_stocks()
    cachedir = '.cache'

    try:
        os.mkdir(cachedir)
    except:
        pass

    for symbol, row in filtered.items():
        table = pa.Table.from_pandas(df)
        pq.write_table(table, f"{cachedir}/{symbol}.parquet")