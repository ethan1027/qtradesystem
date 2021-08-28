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
  pass
