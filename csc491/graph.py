import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def log_returns(dfs, cols):
  fig, axs = plt.subplots(1, len(dfs), figsize=(15, 5))
  fig.suptitle('Log Returns Histogram')

  if len(dfs) == 1:
    axs = [axs]

  for i in range(len(dfs)):
    df = dfs[i]
    df['log_returns'] = np.log(df[cols[i]] / df[cols[i]].shift(1))
    df.dropna(inplace=True)
    axs[i].hist(df['log_returns'], bins=100)
  
  plt.show()

def bar_count(dfs):
  fig, axs = plt.subplots(len(dfs), figsize=(15, 5))
  fig.suptitle('Bar Counts')

  if len(dfs) == 1:
    axs = [axs]

  for i in range(len(dfs)):
    df = dfs[i]
    df = df.groupby(pd.Grouper(level='timestamp', freq='W')).size().rename('count').reset_index()
    axs[i].bar(df['timestamp'], df['count'], width=5)
    axs[i].tick_params(axis='x', rotation=45)

  plt.tight_layout()
  plt.show()