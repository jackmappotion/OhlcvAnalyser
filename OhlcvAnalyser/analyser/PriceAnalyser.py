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

    def get_price_rank(self, prices, price):
        """
        price upper n%
        """
        sorted_purchases = np.sort(np.append(prices, price))
        rank = np.where(sorted_purchases == price)[0][0] + 1
        percentile = round(
            ((len(sorted_purchases) - rank) / len(sorted_purchases)) * 100, 2
        )
        return percentile
