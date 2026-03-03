import transform as tf
import ffd
import graph
import yfinance as yf

i =0
testStrings = ["MSFT", "MU", "MCD", "DDOG", "UBER", "T", "MOBX"]
while i < len(testStrings):
    df = tf.gen_dollar_bars(testStrings)
    print("d value for " + testStrings[i])
    dValue = ffd.get_ffd(df)
    print(dValue)
    i = i+1