class VarianceAnalyser:
    @staticmethod
    def get_variance(series):
        return series.var()

    @staticmethod
    def get_open_close_diff(open_series, close_series):
        open_close_diff = open_series - close_series
        return open_close_diff

    @staticmethod
    def get_open_close_variance(open_series, close_series):
        open_close_diff = VarianceAnalyser.get_open_close_diff(
            open_series, close_series
        )
        open_close_variance = VarianceAnalyser.get_variance(open_close_diff)
        return open_close_variance

    @staticmethod
    def get_normalized_open_close_diff(open_series, close_series):
        normalized_open_close_diff = (open_series - close_series) / open_series
        return normalized_open_close_diff

    @staticmethod
    def get_noramlized_open_close_variance(open_series, close_series):
        normalized_open_close_diff = (
            VarianceAnalyser.get_normalized_open_close_diff(
                open_series, close_series
            )
        )
        normalized_open_close_variance = VarianceAnalyser.get_variance(
            normalized_open_close_diff
        )
        return normalized_open_close_variance

    @staticmethod
    def get_high_low_diff(high_series, low_series):
        high_low_diff = high_series - low_series
        return high_low_diff

    @staticmethod
    def get_high_low_variance(high_series, low_series):
        high_low_diff = VarianceAnalyser.get_high_low_diff(
            high_series, low_series
        )
        high_low_variance = VarianceAnalyser.get_variance(high_low_diff)
        return high_low_variance

    @staticmethod
    def get_normalized_high_low_diff(high_series, low_series):
        normalized_high_low_diff = (high_series - low_series) / high_series
        return normalized_high_low_diff

    @staticmethod
    def get_normalized_high_low_variance(high_series, low_series):
        normalized_high_low_diff = (
            VarianceAnalyser.get_normalized_high_low_diff(
                high_series, low_series
            )
        )
        normalized_high_low_variance = VarianceAnalyser.get_variance(
            normalized_high_low_diff
        )
        return normalized_high_low_variance