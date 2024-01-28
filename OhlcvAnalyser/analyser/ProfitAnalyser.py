import numpy as np
import pandas as pd


class ProfitAnalyser:
    @staticmethod
    def calc_pct(value):
        return round(value * 100, 3)

    def get_start_end_profit(self, price_series):
        """
        (start,end) Profit Calculator
        """
        buying_price = price_series.iloc[0]
        selling_price = price_series.iloc[-1]
        profit = (selling_price - buying_price) / buying_price
        return self.calc_pct(profit)

    def get_start_max_profit(self, price_series):
        """
        (start, max) Max Profit Calculator
        """
        buying_price = price_series.iloc[0]
        max_price = price_series.max()
        max_profit = (max_price - buying_price) / buying_price
        return self.calc_pct(max_profit)

    def get_start_min_profit(self, price_series):
        """
        (start, min) Min Profit Calculator
        """
        buying_price = price_series.iloc[0]
        min_price = price_series.min()
        min_profit = (min_price - buying_price) / buying_price
        return self.calc_pct(min_profit)

    def get_statistical_price_series(self, high_series, low_series):
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
