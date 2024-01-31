import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


class Plotter:
    @staticmethod
    def general_ohlcv_plot(ax: plt.Axes, ohlcv: pd.DataFrame) -> plt.Axes:
        """
        Plot the general OHLCV chart.

        Args:
            ax (plt.Axes): The axes to plot the chart on.
            ohlcv (pd.DataFrame): The OHLCV data.

        Returns:
            plt.Axes: The axes with the plotted chart.
        """
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
    def draw_regression_plot(ax: plt.Axes, ohlcv: pd.DataFrame, slice: int = 1) -> plt.Axes:
        """
        Draw a regression plot for the OHLCV data.

        Args:
            ax (plt.Axes): The axes to plot the chart on.
            ohlcv (pd.DataFrame): The OHLCV data.
            slice (int, optional): The number of slices to divide the data into. Defaults to 1.

        Returns:
            plt.Axes: The axes with the plotted chart.
        """
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
