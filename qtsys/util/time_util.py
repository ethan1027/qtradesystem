from datetime import date, datetime
import pytz


ny_tz = pytz.timezone('US/Eastern')

def get_start_datetime(start_time: str):
  return f'{date.today()} {start_time}:00'

def get_market_now() -> datetime:
  return datetime.now().astimezone(ny_tz)

def get_market_today() -> date:
  return get_market_now().date()
