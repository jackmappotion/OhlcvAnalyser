import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


class Plotter:
    @staticmethod
    def general_ohlcv_plot(ax, ohlcv):
        ax.plot(ohlcv.index, ohlcv["close"], color="black", alpha=0.1)
        ax.fill_between(ohlcv.index, ohlcv["high"], ohlcv["low"], alpha=1)
        ax.scatter(
            ohlcv.index,
            ohlcv["close"],
            color="black",
            s=(ohlcv["volume"] - ohlcv["volume"].min())
            / (ohlcv["volume"].max() - ohlcv["volume"].min())
            * 300,
            alpha=0.3,
        )
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        return ax

    @staticmethod
    def draw_regression_plot(ax, ohlcv, slice=1):
        window = len(ohlcv) // slice
        for idx in range(slice):
            n_volume_series = (
                (ohlcv["volume"] - ohlcv["volume"].min())
                / (ohlcv["volume"].max() - ohlcv["volume"].min())
                * 300
            )
            _volume = n_volume_series.iloc[idx * window : window * (idx + 1)]
            _ohlcv = ohlcv.iloc[idx * window : window * (idx + 1)]
            sns.regplot(
                x=mdates.date2num(_ohlcv.index),
                y=_ohlcv["close"],
                ax=ax,
                scatter_kws={
                    "s": _volume,
                    "alpha": 0.5,
                },
            )
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        return ax
