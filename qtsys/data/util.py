import pandas as pd
from pandas.core.frame import DataFrame


def resample_bar_data(df: DataFrame, interval):
  p = df['price'].resample(interval, origin='start').last()
  o = df['open'].resample(interval, origin='start').first()
  h = df['high'].resample(interval, origin='start').max()
  l = df['low'].resample(interval, origin='start').min()
  c = df['close'].resample(interval, origin='start').last()
  v = df['volume'].resample(interval, origin='start').sum()
  vwap = df['vwap'].resample(interval, origin='start').mean()
  return pd.concat([p, o, h, l, c, v, vwap], axis=1)

