import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller 
from mlfinpy.util.frac_diff import frac_diff_ffd, plot_min_ffd
import json

def get_ffd(df):
    p_value = 0
    diff_amt = 1
    while p_value < .05:
        diff_amt = diff_amt - .01
        thresh = 1e-05
        frac_df = frac_diff_ffd(df, diff_amt, thresh)
        close = frac_df["Close"]
        close = close.dropna()
        result = adfuller(close)
        p_value = result[1]
    return diff_amt
