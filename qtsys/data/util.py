import pandas as pd
from pandas.core.frame import DataFrame


def resample_bar_data(df: DataFrame, interval):
  p = df['price'].resample(interval).last()
  o = df['open'].resample(interval).first()
  h = df['high'].resample(interval).max()
  l = df['low'].resample(interval).min()
  c = df['close'].resample(interval).last()
  v = df['volume'].resample(interval).sum()
  vwap = df['vwap'].resample(interval).mean()
  return pd.concat([p, o, h, l, c, v, vwap], axis=1)

