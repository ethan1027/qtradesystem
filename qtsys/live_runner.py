from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
from datetime import datetime, timedelta, timezone
from qtsys.broker.broker import Broker
from qtsys.data.yahoo_data import YahooData

from qtsys.alpha.alpha_model import AlphaModel
from qtsys.data.market_data import MarketData
from qtsys.portfolio.portfolio_opt import PortfolioOpt
from qtsys.selector.universe_selector import UniverseSelector
from qtsys.portfolio.equal_portfolio_opt import EqualPortfolioOpt
from qtsys.client.iex import IEX


ny_tz = pytz.timezone('US/Eastern')
 
def run(
  alpha_model: AlphaModel,
  universe_selector: UniverseSelector,
  broker: Broker,
  portfolio_opt = EqualPortfolioOpt(),
  interval: str = '1h',
  offset: int = 5,
  selection_interval: str = 'mon-fri',
  market_data=YahooData(),
  iex_data = IEX()
):
  '''

  selection_interval: https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html?highlight=cron#expression-types
  '''
  scheduler = BlockingScheduler()
  selector_params = (universe_selector, iex_data)
  scheduler.add_job(select_assets, 'cron', day_of_week='mon-sun', hour=16, minute=49, timezone='US/Eastern')
  trader_params = (alpha_model, broker, market_data,)
  scheduler.add_job(trade, 'interval', minutes=1, start_date='2021-08-28 13:25:00', timezone='US/Eastern')
  print(scheduler.get_jobs())
  scheduler.start()


def trade(
  alpha_model: AlphaModel,
  broker: Broker, 
  portfolio_opt: PortfolioOpt,
  data: MarketData,
  iex
):
  print(datetime.now(), 'trading job')
  if broker.is_market_open():
    pass
  
def select_assets():
  print(datetime.now(), 'selecting job')
  