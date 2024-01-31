from typing import Union
from datetime import datetime
import pandas as pd

from .analyser import CoefficientAnalyser, ProfitAnalyser, VarianceAnalyser
from .utils import filter_date


class MultiOhlcvAnalyser:
    def __init__(self, multi_ohlcv: pd.DataFrame) -> None:
        """
        Initialize the MultiOhlcvAnalyser class.

        Parameters:
        - multi_ohlcv (pd.DataFrame): The multi-ohlcv data.

        Returns:
        None
        """
        self.ohlcv = multi_ohlcv.copy()

    @staticmethod
    def _get_groupby_code(ohlcv: pd.DataFrame, start: str, end: str):
        """
        Get the groupby object of the ohlcv data based on the code column.

        Parameters:
        - ohlcv (pd.DataFrame): The ohlcv data.
        - start (str): The start date.
        - end (str): The end date.

        Returns:
        pd.core.groupby.generic.DataFrameGroupBy: The groupby object.
        """
        groupby_ohlcv = filter_date(ohlcv, start, end).groupby("code")
        return groupby_ohlcv

    def info(
        self,
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
    ) -> pd.DataFrame:
        """
        Get general information about the multi-ohlcv data.

        Parameters:
        - start (Union[str, datetime]): The start date. Default is None.
        - end (Union[str, datetime]): The end date. Default is None.

        Returns:
        pd.DataFrame: The information dataframe.
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

    def coef(
        self,
        arg: str,
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
    ) -> pd.Series:
        """
        Get the coefficient series for a given argument.

        Parameters:
        - arg (str): The argument to calculate the coefficient.
        - start (Union[str, datetime]): The start date. Default is None.
        - end (Union[str, datetime]): The end date. Default is None.

        Returns:
        pd.Series: The coefficient series.
        """
        groupby_code = self._get_groupby_code(self.ohlcv, start, end)
        coef_series = groupby_code.apply(
            lambda x: CoefficientAnalyser.get_coefficient(x[arg])
        ).rename(f"{arg}_coef")
        return coef_series

    def normalized_coef(
        self,
        arg: str,
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
    ) -> pd.Series:
        """
        Get the normalized coefficient series for a given argument.

        Parameters:
        - arg (str): The argument to calculate the normalized coefficient.
        - start (Union[str, datetime]): The start date. Default is None.
        - end (Union[str, datetime]): The end date. Default is None.

        Returns:
        pd.Series: The normalized coefficient series.
        """
        groupby_code = self._get_groupby_code(self.ohlcv, start, end)
        normalized_coef_series = groupby_code.apply(
            lambda x: CoefficientAnalyser.get_normalized_coefficient(x[arg])
        ).rename(f"{arg}_normalized_coef")
        return normalized_coef_series

    def coef_score(
        self,
        arg: str,
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
    ) -> pd.Series:
        """
        Get the coefficient score series for a given argument.

        Parameters:
        - arg (str): The argument to calculate the coefficient score.
        - start (Union[str, datetime]): The start date. Default is None.
        - end (Union[str, datetime]): The end date. Default is None.

        Returns:
        pd.Series: The coefficient score series.
        """
        groupby_code = self._get_groupby_code(self.ohlcv, start, end)
        coef_score_series = groupby_code.apply(
            lambda x: CoefficientAnalyser.get_coefficient_score(x[arg])
        ).rename(f"{arg}_coef_score")
        return coef_score_series

    def oc_variance(
        self,
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
    ) -> pd.Series:
        """
        Get the (open - close) variance series.

        Parameters:
        - start (Union[str, datetime]): The start date. Default is None.
        - end (Union[str, datetime]): The end date. Default is None.

        Returns:
        pd.Series: The (open - close) variance series.
        """
        groupby_code = self._get_groupby_code(self.ohlcv, start, end)
        oc_variance_series = groupby_code.apply(
            lambda x: VarianceAnalyser.get_normalized_diff_variance(
                x["open"], x["close"]
            )
        ).rename("oc_variance")
        return oc_variance_series

    def hl_variance(
        self,
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
    ) -> pd.Series:
        """
        Get the (high - low) variance series.

        Parameters:
        - start (Union[str, datetime]): The start date. Default is None.
        - end (Union[str, datetime]): The end date. Default is None.

        Returns:
        pd.Series: The (high - low) variance series.
        """
        groupby_code = self._get_groupby_code(self.ohlcv, start, end)
        hl_variance_series = groupby_code.apply(
            lambda x: VarianceAnalyser.get_normalized_diff_variance(
                x["high"], x["low"]
            )
        ).rename("hl_variance")
        return hl_variance_series

    def profit(
        self,
        arg: str = "close",
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
    ) -> pd.Series:
        """
        Get the profit series for a given argument.

        Parameters:
        - arg (str): The argument to calculate the profit. Default is "close".
        - start (Union[str, datetime]): The start date. Default is None.
        - end (Union[str, datetime]): The end date. Default is None.

        Returns:
        pd.Series: The profit series.
        """
        ohlcv = self.ohlcv.copy()
        groupby_code = self._get_groupby_code(ohlcv, start, end)
        profit_series = groupby_code.apply(
            lambda x: ProfitAnalyser.get_start_end_profit(x[arg])
        ).rename("profit")
        return profit_series
