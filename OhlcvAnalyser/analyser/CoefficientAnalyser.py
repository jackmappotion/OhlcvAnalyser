import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

lr = LinearRegression()


class CoefficientAnalyser:
    @staticmethod
    def get_coefficient(series):
        x = np.arange(1, len(series) + 1).reshape(-1, 1)
        y = series.values.reshape(-1, 1)
        lr.fit(x, y)
        coefficient = lr.coef_[0][0]
        return coefficient

    @staticmethod
    def get_coefficient_score(series):
        x = np.arange(1, len(series) + 1).reshape(-1, 1)
        y = series.values.reshape(-1, 1)
        lr.fit(x, y)
        score = lr.score(x, y)
        return score

    @staticmethod
    def get_normalized_coefficient(series):
        normalized_series = series / series.mean()
        normalized_coefficient = CoefficientAnalyser.get_coefficient(
            normalized_series
        )
        return normalized_coefficient

    @staticmethod
    def get_statistical_price_series(high_series, low_series):
        """
        (high, low) based Noramlized distribution assumption
        """
        mean_series = ((high_series + low_series) / 2).rename("mean")
        var_series = ((high_series - low_series) / 4).rename("var")

        def get_value_based_on_normal_dist_assumption(mean, var):
            return np.random.normal(mean, var, 1)[0]

        statistical_price_series = pd.concat(
            [mean_series, var_series], axis=1
        ).apply(
            lambda x: get_value_based_on_normal_dist_assumption(
                x["mean"], x["var"]
            ),
            axis=1,
        )
        return statistical_price_series
