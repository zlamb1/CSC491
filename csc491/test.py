import transform
import ffd
import graph
import yfinance as yf

i =0
testStrings = ["MSFT", "MU", "MCD", "DDOG", "UBER"]
while i < len(testStrings):
    df = yf.download(testStrings[i], start="2020-01-03", end="2023-01-01")
    print("d value for " + testStrings[i])
    ffd.get_ffd(df)
    i = i+1