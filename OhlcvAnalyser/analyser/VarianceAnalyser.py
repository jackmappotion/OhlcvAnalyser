from typing import List, Union
import pandas as pd
class VarianceAnalyser:
    @staticmethod
    def get_variance(series: pd.Series) -> float:
        """
        Calculate the variance of a series.

        Args:
            series (pd.Series): The input series.

        Returns:
            float: The variance of the series.
        """
        return series.var()

    @staticmethod
    def get_diff_series(a_series: pd.Series, b_series: pd.Series) -> pd.Series:
        """
        Calculate the difference series between two input series.

        Args:
            a_series (pd.Series): The first input series.
            b_series (pd.Series): The second input series.

        Returns:
            pd.Series: The difference series.
        """
        diff_series = a_series - b_series
        return diff_series

    @staticmethod
    def get_diff_variance(a_series: pd.Series, b_series: pd.Series) -> float:
        """
        Calculate the variance of the difference series between two input series.

        Args:
            a_series (pd.Series): The first input series.
            b_series (pd.Series): The second input series.

        Returns:
            float: The variance of the difference series.
        """
        diff_series = VarianceAnalyser.get_diff_series(a_series, b_series)
        diff_variance = VarianceAnalyser.get_variance(diff_series)
        return diff_variance

    @staticmethod
    def get_normalized_diff_series(a_series: pd.Series, b_series: pd.Series) -> pd.Series:
        """
        Calculate the normalized difference series between two input series.

        Args:
            a_series (pd.Series): The first input series.
            b_series (pd.Series): The second input series.

        Returns:
            pd.Series: The normalized difference series.
        """
        normalized_diff_series = (
            VarianceAnalyser.get_diff_series(a_series, b_series) / a_series
        )
        return normalized_diff_series

    @staticmethod
    def get_normalized_diff_variance(a_series: pd.Series, b_series: pd.Series) -> float:
        """
        Calculate the variance of the normalized difference series between two input series.

        Args:
            a_series (pd.Series): The first input series.
            b_series (pd.Series): The second input series.

        Returns:
            float: The variance of the normalized difference series.
        """
        normalized_diff_series = VarianceAnalyser.get_normalized_diff_series(
            a_series, b_series
        )
        normalized_variance = VarianceAnalyser.get_variance(
            normalized_diff_series
        )
        return normalized_variance