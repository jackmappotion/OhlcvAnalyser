import pandas as pd
import numpy as np


class PriceAnalyser:
    @staticmethod
    def get_normalized_series(series: pd.Series, n: int = 1) -> pd.Series:
        """
        Get the normalized series by dividing each element by the mean of the series and multiplying it by n.

        Args:
            series (pd.Series): The input series.
            n (int, optional): The multiplier. Defaults to 1.

        Returns:
            pd.Series: The normalized series.
        """
        normalized_series = (series / series.mean()) * n
        return round(normalized_series).astype(int)

    @staticmethod
    def get_general_prices(
        price_series: pd.Series, volume_series: pd.Series
    ) -> np.ndarray:
        """
        Get the general prices based on the price series and volume series.

        Args:
            price_series (pd.Series): The price series.
            volume_series (pd.Series): The volume series.

        Returns:
            np.ndarray: The general prices.
        """
        normalized_volume_series = PriceAnalyser.get_normalized_series(
            volume_series, 10
        )
        prices = np.concatenate(
            (
                price_series.apply(lambda x: [x]) * normalized_volume_series
            ).values
        )
        return prices

    @staticmethod
    def get_statistical_prices(
        high_series: pd.Series, low_series: pd.Series, volume_series: pd.Series
    ) -> np.ndarray:
        """
        Get the statistical prices based on the high series, low series, and volume series.

        Args:
            high_series (pd.Series): The high series.
            low_series (pd.Series): The low series.
            volume_series (pd.Series): The volume series.

        Returns:
            np.ndarray: The statistical prices.
        """
        normalized_volume_series = PriceAnalyser.get_normalized_series(
            volume_series, 10
        )
        mean_series = ((high_series + low_series) / 2).rename("mean")
        var_series = ((high_series - low_series) / 4).rename("var")

        def get_value_based_on_normal_dist_assumption(
            mean: float, var: float, volume: float
        ) -> np.ndarray:
            return np.random.normal(mean, var, int(volume))

        statistical_prices = np.concatenate(
            pd.concat(
                [
                    mean_series,
                    var_series,
                    normalized_volume_series,
                ],
                axis=1,
            )
            .apply(
                lambda x: get_value_based_on_normal_dist_assumption(
                    x["mean"], x["var"], x["volume"]
                ),
                axis=1,
            )
            .values
        )

        return statistical_prices

    @staticmethod
    def get_price_rank(prices: np.ndarray, price: float) -> float:
        """
        Get the price rank based on the prices and a specific price.

        Args:
            prices (np.ndarray): The array of prices.
            price (float): The specific price.

        Returns:
            float: The price rank.
        """
        sorted_prices = np.sort(np.append(prices, price))
        rank = np.where(sorted_prices == price)[0][0] + 1
        percentile = round(
            ((len(sorted_prices) - rank) / len(sorted_prices)) * 100, 2
        )
        return percentile

    @staticmethod
    def _get_pressure_indicator(
        open_price: float, close_price: float
    ) -> float:
        """
        Get the pressure indicator based on the open price and close price.

        Args:
            open_price (float): The open price.
            close_price (float): The close price.

        Returns:
            float: The pressure indicator.
        """
        pressure_indicator = (close_price - open_price) / open_price * 100 * 3
        return pressure_indicator

    @staticmethod
    def get_buying_selling_general_prices(
        open_price: float, close_price: float, volume: pd.Series
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Get the buying and selling general prices based on the open price, close price, and volume.

        Args:
            open_price (float): The open price.
            close_price (float): The close price.
            volume (pd.Series): The volume series.

        Returns:
            tuple[np.ndarray, np.ndarray]: The buying prices and selling prices.
        """
        pressure_indicator = PriceAnalyser._get_pressure_indicator(
            open_price, close_price
        )
        normalized_volume = PriceAnalyser.get_normalized_series(volume, 10)
        buying_normalized_volume = (
            normalized_volume * (100 + pressure_indicator) / 200
        )
        selling_normalized_volume = (
            normalized_volume - buying_normalized_volume
        )
        buying_prices = PriceAnalyser.get_general_prices(
            close_price, buying_normalized_volume
        )
        selling_prices = PriceAnalyser.get_general_prices(
            close_price, selling_normalized_volume
        )
        return buying_prices, selling_prices

    @staticmethod
    def get_buying_selling_statistical_prices(
        open_price: float,
        close_price: float,
        high_price: pd.Series,
        low_price: pd.Series,
        volume: pd.Series,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Get the buying and selling statistical prices based on the open price, close price, high price, low price, and volume.

        Args:
            open_price (float): The open price.
            close_price (float): The close price.
            high_price (pd.Series): The high price series.
            low_price (pd.Series): The low price series.
            volume (pd.Series): The volume series.

        Returns:
            tuple[np.ndarray, np.ndarray]: The buying prices and selling prices.
        """
        pressure_indicator = PriceAnalyser._get_pressure_indicator(
            open_price, close_price
        )
        normalized_volume = PriceAnalyser.get_normalized_series(volume, 10)
        buying_normalized_volume = (
            normalized_volume * (100 + pressure_indicator) / 200
        )
        selling_normalized_volume = (
            normalized_volume - buying_normalized_volume
        )
        buying_prices = PriceAnalyser.get_general_prices(
            close_price, buying_normalized_volume
        )
        selling_prices = PriceAnalyser.get_general_prices(
            close_price, selling_normalized_volume
        )
        return buying_prices, selling_prices
