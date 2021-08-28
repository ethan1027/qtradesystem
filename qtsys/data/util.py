import pandas as pd
from pandas.core.frame import DataFrame


def resample_bar_data(df: DataFrame, interval):
  p = df['price'].resample(interval, origin='start').last() # type: ignore
  o = df['open'].resample(interval, origin='start').first() # type: ignore
  h = df['high'].resample(interval, origin='start').max() # type: ignore
  l = df['low'].resample(interval, origin='start').min() # type: ignore
  c = df['close'].resample(interval, origin='start').last() # type: ignore
  v = df['volume'].resample(interval, origin='start').sum() # type: ignore
  vwap = df['vwap'].resample(interval, origin='start').mean() # type: ignore
  return pd.concat([p, o, h, l, c, v, vwap], axis=1)

