from datetime import datetime, timedelta
from qtsys.broker.broker import Broker
from qtsys.data.yahoo_data import YahooData
import pandas_market_calendars as mcal

from qtsys.alpha.alpha_model import AlphaModel
from qtsys.selector.universe_selector import UniverseSelector
from qtsys.portfolio.equal_portfolio_opt import EqualPortfolioOpt


def run(
  alpha_model: AlphaModel,
  universe_selector: UniverseSelector,
  broker: Broker,
  portfolio_opt=EqualPortfolioOpt(),
  interval=timedelta(hours=1),
  offset=timedelta(minutes=1),
  selection_interval=timedelta(days=1),
  data_provider=YahooData()
):
  nyse = mcal.get_calendar('NYSE')
  now = datetime.now().astimezone(nyse.tz.zone)
  print('bootstrap schedule')
  schedule = _create_schedule(now, nyse)
  while True:
    now = datetime.now().astimezone(nyse.tz.zone)
    if now > schedule.index[-1]:
      print('updating schedule')
      schedule = _create_schedule(now, nyse)
    


def _create_schedule(now, nyse):
  one_month_later = now + timedelta(days=30)
  now_str = datetime.strftime(now, '%Y-%m-%d')
  one_month_later_str = datetime.strftime(one_month_later, '%Y-%m-%d')
  schedule = nyse.schedule(now_str, one_month_later_str) 
  print(schedule)
  return schedule
 
    