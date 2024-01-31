import numpy as np
import pandas as pd


class ProfitAnalyser:
    @staticmethod
    def calc_pct(value: float) -> float:
        """
        Calculate the percentage value of a given number.
        
        Args:
            value (float): The number to calculate the percentage of.
        
        Returns:
            float: The percentage value of the given number.
        """
        return round(value * 100, 3)

    @staticmethod
    def get_start_end_profit(price_series: pd.Series) -> float:
        """
        Calculate the profit percentage between the first and last prices in a price series.
        
        Args:
            price_series (pd.Series): The price series.
        
        Returns:
            float: The profit percentage.
        """
        buying_price = price_series.iloc[0]
        selling_price = price_series.iloc[-1]
        profit = (selling_price - buying_price) / buying_price
        return ProfitAnalyser.calc_pct(profit)

    @staticmethod
    def get_start_max_profit(price_series: pd.Series) -> float:
        """
        Calculate the maximum profit percentage between the first price and the highest price in a price series.
        
        Args:
            price_series (pd.Series): The price series.
        
        Returns:
            float: The maximum profit percentage.
        """
        buying_price = price_series.iloc[0]
        max_price = price_series.max()
        max_profit = (max_price - buying_price) / buying_price
        return ProfitAnalyser.calc_pct(max_profit)

    @staticmethod
    def get_start_min_profit(price_series: pd.Series) -> float:
        """
        Calculate the minimum profit percentage between the first price and the lowest price in a price series.
        
        Args:
            price_series (pd.Series): The price series.
        
        Returns:
            float: The minimum profit percentage.
        """
        buying_price = price_series.iloc[0]
        min_price = price_series.min()
        min_profit = (min_price - buying_price) / buying_price
        return ProfitAnalyser.calc_pct(min_profit)

    @staticmethod
    def get_statistical_price_series(high_series: pd.Series, low_series: pd.Series) -> pd.Series:
        """
        Generate a statistical price series based on the high and low series.
        
        Args:
            high_series (pd.Series): The high price series.
            low_series (pd.Series): The low price series.
        
        Returns:
            pd.Series: The generated statistical price series.
        """
        mean_series = ((high_series + low_series) / 2).rename("mean")
        var_series = ((high_series - low_series) / 4).rename("var")

        def get_value_based_on_normal_dist_assumption(mean: float, var: float) -> float:
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
