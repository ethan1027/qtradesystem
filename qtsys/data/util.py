from pandas.core.frame import DataFrame


def resample_bar_data(df: DataFrame, interval):
  high = df['high'].resample(interval).max()
  low = df['low'].resample(interval).min()
  open = df['open'].resample(interval).first()
  close = df['close'].resample(interval).last()
  print(high)
  print(close)
