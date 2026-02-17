import pandas as pd

from contextlib import closing

def gen_dollar_bars(dataFrame):
  close_price = 0.00
  stocks = 0
  closing_prices = dataFrame[["close", "volume"]]
  rows = closing_prices.size / 2
  bars_index = 1
  bars = []
  current_dollars = 0.00
  index = 0

  while index < rows:
      price = closing_prices['close']
      close_price = price.get(index)
      volume = closing_prices['volume']
      stocks = volume.get(index)
      current_dollars = close_price * stocks
      index += 1
      if current_dollars >= 255800000: #placeholder until strategist number is determined
          bar = {
              'index' : bars_index,
              'price' : close_price
          }
          bars.append(bar)
          bars_index += 1
          current_dollars = 0

  dollar_bars = pd.DataFrame(bars)
  return dollar_bars