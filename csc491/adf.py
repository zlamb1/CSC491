import numpy as np
import pandas as pd

from statsmodels.tsa.stattools import adfuller

def adf(series):
    _adf = adfuller(series)
    return {
        'stat': _adf[0],
        'p_value': _adf[1]
    }

def test(series):
    _adf = adf(series)
    print(f'ADF : {_adf["stat"]}')
    print(f'p-value : {_adf["p_value"]}')

if __name__ == '__main__':
    np.random.seed(0)
    data = np.random.normal(0, 1, 100).cumsum()
    series = pd.Series(data)
    test(series)