import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import csc491
from db import top_1000 as top1000
import os
# hello
directory = "cache"

def make_files():
  try:
    os.mkdir(directory)
  except FileExistsError: 
    pass
  top_stocks = top1000.get()
  for symbol in top_stocks:
    df = csc491.api.get_ticker_data(symbol)
    db = csc491.transform.gen_dollar_bars(df)
    db2 = csc491.ffd.get_ffd(df)
    table1 = pa.Table.from_pandas(df)
    table2 = pa.Table.from_pandas(db)
    table3 = pa.Table.from_pandas(db2)
    pq.write_table(table1, f"{directory}/{symbol}.parquet")
    pq.write_table(table2, f"{directory}/{symbol}_db.parquet")
    pq.write_table(table3, f"{directory}/{symbol}_ffd.parquet")

def get_dollarbar_dataframe(symbol):
  table = pq.read_table(f"{directory}/{symbol}_db.parquet")
  df = table.to_pandas()
  cleaned_df = df.dropna()
  #hdghdghdg
  return cleaned_df

def get_dollarbars_as_series(symbol):
  table = pq.read_table(f"{directory}/{symbol}_db.parquet")
  df = table.to_pandas()
  cleaned_df = df.dropna()
  series = cleaned_df['close']
  return series

def get_ffd_dataframe(symbol):
  table = pq.read_table(f"{directory}/{symbol}_ffd.parquet")
  df = table.to_pandas()
  cleaned_df = df.dropna()
  return cleaned_df

def get_raw_dataframe(symbol):
  table = pq.read_table(f"{directory}/{symbol}.parquet")
  df = table.to_pandas()
  cleaned_df = df.dropna()
  return cleaned_df



if __name__ == '__main__':
  make_files()