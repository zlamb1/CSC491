import pandas as pd
import numpy as np
import json

from csc491 import adf
from mlfinpy.util.frac_diff import frac_diff_ffd, plot_min_ffd

def _mid(low, high):
    return low+(high-low)/2

def get(df, target=.05, thresh=1e-05, max_attempts=10):
    low = 0
    high = 1
    mid = _mid(low, high)
    attempts = 0

    best = None

    # Perform a binary search looking for the smallest d-value that produces a p-value <= target.

    while attempts < max_attempts:
        frac_df = frac_diff_ffd(df, mid, thresh)
        close = frac_df['close'].dropna()
        # adfuller can't process constant series; skip if we don't have enough data
        if len(close) == 1:
            continue
        p_value = adf.get(close)['p_value']

        if p_value <= target:
            high = mid
            best = { 'df': frac_df, 'd_value': mid, 'p_value': p_value }
        else:
            low = mid

        mid = _mid(low, high)
        attempts += 1

    if best is None:
        raise RuntimeError('Could not find stationary d-value for data set.')

    return { 'df': best['df'], 'd_value': best['d_value'] }
