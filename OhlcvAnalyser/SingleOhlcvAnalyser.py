import pandas as pd

from .analyser import ProfitAnalyser, PriceAnalyser, CoefficientAnalyser
from .utils import filter_date

class SingleOhlcvAnalyser:
    def __init__(self, single_ohlcv: pd.DataFrame):
        """
        Initialize the SingleOhlcvAnalyser class.

        Parameters:
        - single_ohlcv (pd.DataFrame): The OHLCV data for a single stock.

        """
        self.ohlcv = single_ohlcv.copy()

    def info(self, start=None, end=None) -> pd.DataFrame:
        """
        Get information about the OHLCV data.

        Parameters:
        - start (str or None): The start date for filtering the data. Default is None.
        - end (str or None): The end date for filtering the data. Default is None.

        Returns:
        - pd.DataFrame: A DataFrame containing the information about the OHLCV data.

        """
        ohlcv = filter_date(self.ohlcv, start, end)
        info_dict = {
            "stock_code": ohlcv["code"].iloc[0],
            "start_date": ohlcv.index.min(),
            "end_date": ohlcv.index.max(),
            "start_end_profit": ProfitAnalyser.get_start_end_profit(
                ohlcv["close"]
            ),
            "start_max_profit": ProfitAnalyser.get_start_max_profit(
                ohlcv["close"]
            ),
            "start_min_profit": ProfitAnalyser.get_start_min_profit(
                ohlcv["close"]
            ),
        }
        info_df = pd.DataFrame.from_dict(
            info_dict, orient="index", columns=["value"]
        )
        return info_df


    def get_price_rank_series(self, start: str, end: str, price: float) -> pd.Series:
        """
        Get the price rank series for a given date range and price.

        Parameters:
        - start (str): The start date for filtering the data.
        - end (str): The end date for filtering the data.
        - price (float): The price for calculating the price rank.

        Returns:
        - pd.Series: A Series containing the price rank information.

        """
        filtered_ohlcv = filter_date(self.ohlcv, start, end)
        statistical_prices = PriceAnalyser.get_statistical_prices(
            filtered_ohlcv["high"],
            filtered_ohlcv["low"],
            filtered_ohlcv["volume"],
        )
        price_rank_series = pd.Series(
            {
                "start_date": start.strftime("%Y-%m-%d"),
                "date_diff": (end - start).days,
                "end_date": end.strftime("%Y-%m-%d"),
                "price": price,
                "mean_price": round(statistical_prices.mean(), 2),
                "price_rank": PriceAnalyser.get_price_rank(
                    statistical_prices, price
                ),
            }
        )
        return price_rank_series

    def get_coefficient_series(self, arg: str, start: str, end: str) -> pd.Series:
        """
        Get the coefficient series for a given argument, start date, and end date.

        Parameters:
        - arg (str): The argument for calculating the coefficient.
        - start (str): The start date for filtering the data.
        - end (str): The end date for filtering the data.

        Returns:
        - pd.Series: A Series containing the coefficient information.

        """
        filtered_ohlcv = filter_date(self.ohlcv, start, end)
        coefficient_series = pd.Series(
            {
                "start_date": start.strftime("%Y-%m-%d"),
                "date_diff": (end - start).days,
                "end_date": end.strftime("%Y-%m-%d"),
                "arg": arg,
                "coefficient": CoefficientAnalyser.get_normalized_coefficient(
                    filtered_ohlcv[arg]
                ),
            }
        )
        return coefficient_series