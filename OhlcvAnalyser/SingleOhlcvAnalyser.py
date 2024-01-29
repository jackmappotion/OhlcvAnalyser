import pandas as pd

from .analyser import ProfitAnalyser, PriceAnalyser, CoefficientAnalyser
from .utils import filter_date

class SingleOhlcvAnalyser:
    def __init__(self, single_ohlcv):
        self.ohlcv = single_ohlcv.copy()

    def info(self, start=None, end=None):
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

    @staticmethod
    def get_price_rank_series(ohlcv, start, end, price):
        filtered_ohlcv = filter_date(ohlcv, start, end)
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

    @staticmethod
    def get_coefficient_series(ohlcv, arg, start, end):
        filtered_ohlcv = filter_date(ohlcv, start, end)
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