import pandas as pd

from .analyser import CoefficientAnalyser
from .analyser import ProfitAnalyser
from .utils import filter_date


class MultiOhlcvAnalyser:
    def __init__(self, multi_ohlcv) -> None:
        self.ohlcv = multi_ohlcv.copy()

    @staticmethod
    def _get_groupby_code(ohlcv, start, end):
        groupby_ohlcv = filter_date(ohlcv, start, end).groupby("code")
        return groupby_ohlcv

    def info(self, start=None, end=None):
        """
        General Information
        """
        ohlcv = filter_date(self.ohlcv, start, end)
        groupby_code = self._get_groupby_code(ohlcv, start, end)
        profit_row = groupby_code.apply(
            lambda x: ProfitAnalyser.get_start_end_profit(x["close"])
        )
        info_dict = {
            "total_stock_code": len(set(ohlcv["code"])),
            "start_date": ohlcv.index.min(),
            "end_date": ohlcv.index.max(),
            "market_average_profit": (profit_row.mean().round(2)),
            "increased_stock_pct": round(
                len(profit_row[profit_row > 0]) / len(profit_row), 2
            )
            * 100,
            "decreased_stock_pct": round(
                len(profit_row[profit_row <= 0]) / len(profit_row), 2
            )
            * 100,
        }

        info_df = pd.DataFrame.from_dict(
            info_dict, orient="index", columns=["value"]
        )
        return info_df

    def coef(self, arg, start=None, end=None):
        """
        Series : coefficient
        """
        groupby_code = self._get_groupby_code(self.ohlcv, start, end)
        coef_series = groupby_code.apply(
            lambda x: CoefficientAnalyser.get_coefficient(x[arg])
        ).rename(f"{arg}_coef")
        return coef_series

    def normalized_coef(self, arg, start=None, end=None):
        """
        Series / Series.mean() : coefficient
        """
        groupby_code = self._get_groupby_code(self.ohlcv, start, end)
        normalized_coef_series = groupby_code.apply(
            lambda x: CoefficientAnalyser.get_normalized_coefficient(x[arg])
        ).rename(f"{arg}_normalized_coef")
        return normalized_coef_series

    def oc_variance(self, start, end):
        """
        (open - close) variance
        """
        ohlcv = self.ohlcv.copy()
        ohlcv["oc_change"] = (ohlcv["open"] - ohlcv["close"]) / ohlcv["open"]
        groupby_code = self._get_groupby_code(ohlcv, start, end)
        oc_variance_series = groupby_code.apply(
            lambda x: x["oc_change"].var()
        ).rename("oc_variance")
        return oc_variance_series

    def hl_variance(self, start, end):
        """
        (high - low) variance
        """
        ohlcv = self.ohlcv.copy()
        ohlcv["hl_change"] = (ohlcv["high"] - ohlcv["low"]) / ohlcv["low"]
        groupby_code = self._get_groupby_code(ohlcv, start, end)
        hl_variance_series = groupby_code.apply(
            lambda x: x["hl_change"].var()
        ).rename("hl_variance")
        return hl_variance_series

    def profit(self, start, end):
        ohlcv = self.ohlcv.copy()
        groupby_code = self._get_groupby_code(ohlcv, start, end)
        profit_series = groupby_code.apply(
            lambda x: ProfitAnalyser.get_start_end_profit(x)
        ).rename("profit")
        return profit_series
