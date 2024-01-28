def filter_date(ohlcv, start, end):
    filtered_ohlcv = ohlcv.copy()
    if start:
        filtered_ohlcv = filtered_ohlcv[start <= filtered_ohlcv.index]
    if end:
        filtered_ohlcv = filtered_ohlcv[filtered_ohlcv.index <= end]
    return filtered_ohlcv
