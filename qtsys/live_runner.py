from time import time
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
from datetime import datetime, timedelta, timezone
from qtsys.broker.broker import Broker
from qtsys.data.yahoo_data import YahooData
import pandas_market_calendars as mcal

from qtsys.alpha.alpha_model import AlphaModel
from qtsys.selector.universe_selector import UniverseSelector
from qtsys.portfolio.equal_portfolio_opt import EqualPortfolioOpt


ny_tz = pytz.timezone('US/Eastern')
 
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
  scheduler = BlockingScheduler()
  scheduler.add_job(selecting, 'cron', day_of_week='mon-sun', hour=16, minute=49, timezone='US/Eastern')
  scheduler.add_job(trading, 'interval', minutes=1, start_date='2021-08-28 13:25:00', timezone='US/Eastern')
  print(scheduler.get_jobs())
  scheduler.start()


def trading(broker: Broker, data):
  print(datetime.now(), 'trading job')
  if broker.is_market_open():
    pass
  
def selecting():
  print(datetime.now(), 'selecting job')
  