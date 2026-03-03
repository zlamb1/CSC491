import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import csc491
from db import top_1000 as top1000
# hello

def make_files():
  top_stocks = top1000.get()
  for symbol in top_stocks:
    df = csc491.api.get_ticker_data(symbol)
    db = csc491.transform.gen_dollar_bars(df)
    db2 = csc491.ffd.get_ffd(df)
    table = pa.Table.from_pandas(db)
    table2 = pa.Table.from_pandas(db2)
    pq.write_table(table, f"{symbol}.parquet")
    pq.write_table(table2, f"{symbol}_ffd.parquet")

def get_dollarbar_dataframe(symbol):
  table = pq.read_table(f"{symbol}.parquet")
  df = table.to_pandas()
  cleaned_df = df.dropna()
  #hdghdghdg
  return cleaned_df

def get_dollarbars_as_series(symbol):
  table = pq.read_table(f"{symbol}.parquet")
  df = table.to_pandas()
  cleaned_df = df.dropna()
  series = cleaned_df['close']
  return series

def get_ffd_dataframe(symbol):
  table = pq.read_table(f"{symbol}_ffd.parquet")
  df = table.to_pandas()
  cleaned_df = df.dropna()
  return cleaned_df

if __name__ == '__main__':
  make_files()