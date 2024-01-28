# Coef
import numpy as np
from sklearn.linear_model import LinearRegression

def get_linear_coef(series):
    lr = LinearRegression()
    x = np.arange(1, len(series) + 1).reshape(-1, 1)
    y = series.values.reshape(-1, 1)
    lr.fit(x, y)
    coef = lr.coef_[0][0]
    return coef


def get_normalized_linear_coef(series):
    normalized_series = series / series.mean()
    return get_linear_coef(normalized_series)