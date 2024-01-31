import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

lr = LinearRegression()


class CoefficientAnalyser:
    @staticmethod
    def get_coefficient(series: pd.Series) -> float:
        """
        Calculates the coefficient of a series using linear regression.

        Args:
            series (pd.Series): The input series.

        Returns:
            float: The coefficient value.
        """
        x = np.arange(1, len(series) + 1).reshape(-1, 1)
        y = series.values.reshape(-1, 1)
        lr.fit(x, y)
        coefficient = lr.coef_[0][0]
        return coefficient

    @staticmethod
    def get_coefficient_score(series: pd.Series) -> float:
        """
        Calculates the coefficient score of a series using linear regression.

        Args:
            series (pd.Series): The input series.

        Returns:
            float: The coefficient score value.
        """
        x = np.arange(1, len(series) + 1).reshape(-1, 1)
        y = series.values.reshape(-1, 1)
        lr.fit(x, y)
        score = lr.score(x, y)
        return score

    @staticmethod
    def get_normalized_coefficient(series: pd.Series) -> float:
        """
        Calculates the normalized coefficient of a series using linear regression.

        Args:
            series (pd.Series): The input series.

        Returns:
            float: The normalized coefficient value.
        """
        normalized_series = series / series.mean()
        normalized_coefficient = CoefficientAnalyser.get_coefficient(
            normalized_series
        )
        return normalized_coefficient