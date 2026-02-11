import pandas as pd
import matplotlib.pyplot as plt

print('Stock Ticker: ', end='')
stock_ticker = input()

# Pod A: Data Curator & Feature Analyst

#
# Step 1: Fetch the data from an API. Put it into a Pandas DataFrame.
# This can be done using alpaca or yfinance.
#

#
# Step 2: Sanitize the data by removing any bad entries (containing NaN) and renaming columns.
# Expected columns are [data, close, volume].
#

#
# Step 3: Calculate the simple moving average over 50 days. 
# Append it to the data frame as the SMA_50 column.
#

#
# Step 4: Calculate the relative strength index (RSI) over 14 days.
# Append it to the data frame as the RSI_14 column. 
#

# Pod B: Strategist & Backtester

#
# Step 1: Determine the conditions. What is the minimum SMA/EMA/RSI before we buy?
# What is the maximum SMA/EMA/RSI before we sell? Do we have any other signals we want
# to use?
#

# SMA/RSI minimum values before we buy.
sma_buy = 0
rsi_buy = 0

# SMA/RSI maximum values before we sell.
sma_sell = 0
rsi_sell = 0

#
# Step 2: Implement the generate_signals function that takes a data frame and performs some
# action based on the conditions we established. This function should decide the trading policy.
# How much will we spend each time we buy?
#

# How much money we have.
balance = 100_000

# How many stocks we have bought.
stocks = 0

def generate_signals(df):
    pass

generate_signals(None)

print(f'Balance: ${balance}')
print(f'Stocks Bought ({stock_ticker}): {stocks}')