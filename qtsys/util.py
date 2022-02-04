from datetime import date, datetime
import pandas as pd
import pytz


ny_tz = pytz.timezone('US/Eastern')

def get_start_datetime(start_time: str):
  return f'{date.today()} {start_time}:00'

def get_market_now() -> datetime:
  return datetime.now().astimezone(ny_tz)

def get_market_today() -> date:
  return get_market_now().date()

def resample_bar_data(df: pd.DataFrame, interval):
  p = df['price'].resample(interval, origin='start').last()
  o = df['open'].resample(interval, origin='start').first()
  h = df['high'].resample(interval, origin='start').max()
  l = df['low'].resample(interval, origin='start').min()
  c = df['close'].resample(interval, origin='start').last()
  v = df['volume'].resample(interval, origin='start').sum()
  vwap = df['vwap'].resample(interval, origin='start').mean()
  return pd.concat([p, o, h, l, c, v, vwap], axis=1)
