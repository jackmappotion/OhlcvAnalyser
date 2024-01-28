def calc_profit(series):
    profit = (series.iloc[-1] - series.iloc[0]) / series.iloc[0]
    return profit
