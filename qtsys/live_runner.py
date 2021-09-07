from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
from datetime import datetime, timedelta, timezone
from qtsys.broker.broker import Broker

from qtsys.alpha.alpha_model import AlphaModel
from qtsys.data.market_data import MarketData
from qtsys.portfolio.portfolio_opt import PortfolioOpt
from qtsys.selector.universe_selector import UniverseSelector
from qtsys.portfolio.equal_portfolio_opt import EqualPortfolioOpt
from qtsys.data.data_bundle import DataBundle


ny_tz = pytz.timezone('US/Eastern')

def run(
  alpha_model: AlphaModel,
  universe_selector: UniverseSelector,
  broker: Broker,
  portfolio_opt = EqualPortfolioOpt(),
  interval: str = '1h',
  offset: int = 5,
  selection_day: str = 'mon-fri',
  market_data: str = 'tradier',
):
  '''
    selection_interval: https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html?highlight=cron#expression-types
  '''
  data_bundle = DataBundle()
  scheduler = BlockingScheduler()
  selector_params = (universe_selector, data_bundle)
  scheduler.add_job(
    select_assets, 'cron', selector_params,
    day_of_week=selection_day, hour=16, minute=49, timezone='US/Eastern')
  trader_params = (alpha_model, broker, portfolio_opt, getattr(data_bundle, market_data), data_bundle)
  scheduler.add_job(trade, 'interval', trader_params,
    minutes=1, start_date=_start_time(), timezone='US/Eastern')
  print(scheduler.get_jobs())
  scheduler.start()


def trade(
  alpha_model: AlphaModel,
  broker: Broker,
  portfolio_opt: PortfolioOpt,
  data: MarketData,
  data_bundle: DataBundle
):
  print(datetime.now(), 'trading job')
  if broker.is_market_open():
    pass
  
def select_assets(unviverse_selector: UniverseSelector, data_bundle: DataBundle):
  print(datetime.now(), 'selecting job')
  selection = unviverse_selector.select(data_bundle)
  print(selection)

def _start_time():
  return datetime.now().strftime('%Y-%m-%d 09:30:00')
