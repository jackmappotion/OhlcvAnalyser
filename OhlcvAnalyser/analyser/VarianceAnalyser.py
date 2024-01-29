class VarianceAnalyser:
    @staticmethod
    def get_variance(series):
        return series.var()

    @staticmethod
    def get_diff_series(a_series, b_series):
        diff_series = a_series - b_series
        return diff_series

    @staticmethod
    def get_diff_variance(a_series, b_series):
        diff_series = VarianceAnalyser.get_diff_series(a_series, b_series)
        diff_variance = VarianceAnalyser.get_variance(diff_series)
        return diff_variance

    @staticmethod
    def get_normalized_diff_series(a_series, b_series):
        normalized_diff_series = (
            VarianceAnalyser.get_diff_series(a_series, b_series) / a_series
        )
        return normalized_diff_series

    @staticmethod
    def get_normalized_diff_variance(a_series, b_series):
        normalized_diff_series = VarianceAnalyser.get_normalized_diff_series(
            a_series, b_series
        )
        normalized_variance = VarianceAnalyser.get_variance(
            normalized_diff_series
        )
        return normalized_variance