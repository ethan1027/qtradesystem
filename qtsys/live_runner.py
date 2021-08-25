import math
import time
import pytz
import pandas as pd
from datetime import datetime, timedelta, timezone
from qtsys.broker.broker import Broker
from qtsys.data.yahoo_data import YahooData
import pandas_market_calendars as mcal

from qtsys.alpha.alpha_model import AlphaModel
from qtsys.selector.universe_selector import UniverseSelector
from qtsys.portfolio.equal_portfolio_opt import EqualPortfolioOpt


ny_tz = pytz.timezone('US/Eastern')
        
def _now(): return datetime.now().astimezone(ny_tz)

def _create_schedule():
  now = datetime.now()
  nyse = mcal.get_calendar('NYSE')
  one_month_later = now + timedelta(days=30)
  now_str = datetime.strftime(now, '%Y-%m-%d')
  one_month_later_str = datetime.strftime(one_month_later, '%Y-%m-%d')
  schedule = nyse.schedule(now_str, one_month_later_str)
  return schedule
 
def run(
  alpha_model: AlphaModel,
  universe_selector: UniverseSelector,
  broker: Broker,
  portfolio_opt=EqualPortfolioOpt(),
  interval: timedelta = timedelta(hours=1),
  offset: timedelta = timedelta(minutes=1),
  selection_interval: timedelta = timedelta(days=1),
  market_data=YahooData(),

):
  print('bootstrap schedule')
  schedule = _create_schedule()
  selection_date = None
  while True:
    today = pd.Timestamp(_now().date()) 
    if today > schedule.index[-1]:
      print('updating schedule')
      schedule = _create_schedule()
    if today not in schedule.index:
      print(_now(), 'not a trading day. sleep for an hour...')
      time.sleep(3600)
    else:
      #SElECTING
      if not selection_date or selection_date + selection_interval <= datetime.now().date():
        while _now().hour < 7:
          print(_now(), 'waiting for selection time. sleep for a minute')
          time.sleep(60)
        print(_now(), 'selecting assets')
        selection_date = _now().date()
        # selection = universe_selector.on_selection(selection_date.strftime('%Y-m-%d'))

      # TRADING
      today = _now().strftime('%Y-%m-%d')
      next_trading_time = schedule.loc[today]['market_open'].astimezone(ny_tz) + offset
      closing_time = schedule.loc[today]['market_close'].astimezone(ny_tz)
      if _now() > next_trading_time:
        next_trading_time += math.ceil((_now() - next_trading_time) / interval) * interval
      print('next trading time', next_trading_time)
      while next_trading_time < closing_time:
        if _now() >= next_trading_time:
          print(_now(), 'trading in action')
          next_trading_time += interval
          time.sleep(interval.total_seconds() - 60)
        time.sleep(1)
