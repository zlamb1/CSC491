import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller 
from mlfinpy.util.frac_diff import frac_diff_ffd, plot_min_ffd


data = np.random.normal(0, 1, 100).cumsum()
df = pd.DataFrame(data)
diff_amt = 1
thresh = 1e-05


frac_df = frac_diff_ffd(df, diff_amt, thresh)
print(frac_df)
#plot_min_ffd(frac_df)