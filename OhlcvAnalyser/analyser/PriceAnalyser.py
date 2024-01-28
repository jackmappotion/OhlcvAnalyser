import numpy as np
import pandas as pd


class PriceAnalyser:
    @staticmethod
    def get_normalized_series(series, n=1):
        noramlized_series = (series / series.mean()) * n
        return round(noramlized_series).astype(int)

    @staticmethod
    def get_general_prices(price_series, volume_series):
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
    def get_statistical_prices(high_series, low_series, volume_series):
        normalized_volume_series = PriceAnalyser.get_normalized_series(
            volume_series, 10
        )
        mean_series = ((high_series + low_series) / 2).rename("mean")
        var_series = ((high_series - low_series) / 4).rename("var")

        def get_value_based_on_normal_dist_assumption(mean, var, volume):
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
    def get_price_rank(prices, price):
        """
        price upper n%
        """
        sorted_purchases = np.sort(np.append(prices, price))
        rank = np.where(sorted_purchases == price)[0][0] + 1
        percentile = round(
            ((len(sorted_purchases) - rank) / len(sorted_purchases)) * 100, 2
        )
        return percentile

    @staticmethod
    def _get_pressure_indicator(open_price, close_price):
        pressure_indicator = (close_price - open_price) / open_price * 100 * 3
        return pressure_indicator

    @staticmethod
    def get_buying_selling_general_prices(open_price, close_price, volume):
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
        return (buying_prices, selling_prices)

    @staticmethod
    def get_buying_selling_statistical_prices(
        open_price, close_price, high_price, low_price, volume
    ):
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
        buying_prices = PriceAnalyser.get_statistical_prices(
            high_price, low_price, buying_normalized_volume
        )
        selling_prices = PriceAnalyser.get_statistical_prices(
            high_price, low_price, selling_normalized_volume
        )
        return (buying_prices, selling_prices)
