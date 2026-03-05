import json
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import sys
import threading

from csc491 import api, transform, ffd
from datetime import datetime
from db import top_1000 as top1000
from enum import StrEnum

cachedir = ".cache"

class DataType(StrEnum):
  Raw = ''
  DollarBars = '_db'
  FFD = '_ffd'

def _get_path(symbol, data_type=DataType.Raw):
  return f'{cachedir}/{symbol}{data_type}.parquet'

def _exists(symbol, data_type):
  return os.path.isfile(_get_path(symbol, data_type))

def _get(symbol, data_type):
  if not _exists(symbol, data_type):
    return None 
  table = pq.read_table(_get_path(symbol, data_type))
  df = table.to_pandas()
  return df.dropna()

def get(symbol, data_type=DataType.Raw):
  return _get(symbol, data_type=data_type)

def make_cache_dir(cachedir=cachedir):
  try:
    os.mkdir(cachedir)
  except FileExistsError: 
    # Make sure it is a directory. 
    if not os.path.isdir(cachedir):
      raise RuntimeError(f'{cachedir} must be a directory.')

def _task(tid, func, data_type, total, shared, symbols, log):
  for symbol in symbols:
    with shared['lock']:
      count = shared['count']
      shared['count'] = count + 1
    exists = _exists(symbol, data_type)
    if log:
      s = f' [Cached]' if exists else '' 
      print(f'{count}/{total}: {symbol}{s}')
    if exists:
      continue
    df = func(symbol)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, _get_path(symbol, data_type))

def _make(func, data_type, log=False, thread_count=os.cpu_count()):
  make_cache_dir()
  symbols = top1000.get()
  n = len(symbols)
  thread_count = max(thread_count, 1)
  per_thread = n // thread_count
  threads = []

  shared = {'count': 1, 'lock': threading.Lock()}

  # Assign work to the threads.
  thread_symbols = [[] for _ in range(thread_count)]
  for i in range(n):
    thread_symbols[i % thread_count].append(symbols[i])

  for tid in range(thread_count):
    base = tid * per_thread
    thread = threading.Thread(target=_task, args=(tid, func, data_type, n, shared, thread_symbols[tid], log))
    thread.start()
    threads.append(thread)

  for thread in threads:
    thread.join()

def make_raw(start=datetime(2022, 1, 1), log=False, thread_count=os.cpu_count()//2):
  f = lambda symbol : api.get_ticker_data(symbol, start=start)
  _make(f, DataType.Raw, log=log, thread_count=thread_count)

def make_db(log=False):
  f = lambda symbol : transform.gen_dollar_bars(get(symbol, DataType.Raw))
  _make(f, DataType.DollarBars, log=log)

def make_ffd(log=False, thread_count=1):
  f = lambda symbol : ffd.get(get(symbol, DataType.DollarBars))['df']
  _make(f, DataType.FFD, log=log, thread_count=thread_count)

def make_ffd_json(outfile=f'{cachedir}/ffd.json', log=False):
  make_cache_dir()
  symbols = top1000.get()
  n = len(symbols)
  d_values = {}
  for i in range(n):
    symbol = symbols[i]
    if log:
      print(f'{i}/{n}: [{symbol}]')
    d_value = ffd.get(get(symbol, DataType.DollarBars))['d_value']
    d_values[symbol] = d_value
  with open(outfile, 'w') as f:
    json.dump(d_values, f, indent=4)

def make(data_type, log=False):
  if data_type == DataType.Raw:
    make_raw(log=log)
  elif data_type == DataType.DollarBars:
    make_db(log=log)
  elif data_type == DataType.FFD:
    make_ffd(log=log)
  else:
    raise RuntimeError(f'Unsupported data type \'{data_type}\'')

if __name__ == '__main__':
  args = sys.argv
  if len(args) > 1:
    data_type_arg = args[1]
  else:
    data_type_arg = None

  data_type = DataType.Raw

  if data_type_arg == 'raw':
    pass
  elif data_type_arg == 'db' or data_type_arg == 'dollarbars':
    data_type = DataType.DollarBars
  elif data_type_arg == 'ffd':
    data_type = DataType.FFD
  elif data_type_arg == 'ffd-json':
    make_ffd_json(log=True)
    sys.exit(0)
  elif not data_type_arg is None:
    raise RuntimeError(f'Unknown data type \'{data_type_arg}\'')

  if data_type == DataType.Raw:
    make_raw(log=True)
  elif data_type == DataType.DollarBars:
    make_db(log=True)
  elif data_type == DataType.FFD:
    make_ffd(log=True)
  else:
    raise RuntimeError(f'Unsupported data type \'{data_type}\'')