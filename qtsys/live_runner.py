from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
from datetime import datetime, date, timedelta
from qtsys.broker.broker import Broker

from qtsys.alpha.alpha_model import AlphaModel
from qtsys.broker.order_resolver import OrderResolver
from qtsys.data.market_data import MarketData
from qtsys.screener.asset_screener import AssetScreener
from qtsys.sizer.position_sizer import PositionSizer
from qtsys.sizer.equal_position_sizer import EqualPositionSizer
from qtsys.data.data_bundle import DataBundle
from qtsys.client import pystorew


ny_tz = pytz.timezone('US/Eastern')

def trade(
  alpha_model: AlphaModel,
  broker: Broker,
  position_sizer: PositionSizer,
  data: MarketData,
  interval: str,
  lookback_days: int
):
  print(datetime.now(), 'trading job')
  if broker.is_market_open():
    order_resolver = OrderResolver()
    positions = broker.get_positions()

    # GET ASSETS FROM SCREENER
    symbols = pystorew.read_selection(broker.get_account_id(), date.today())
    order_resolver.set_closing_orders(symbols, positions)

    # RUN ALPHA MODEL
    quotes = data.get_quotes(symbols)
    start = date.today() - timedelta(days=lookback_days)
    historical_bars = data.download_bars(symbols, str(start), str(date.today()), interval)
    new_orders = alpha_model.run_trades(symbols, quotes, historical_bars, positions, order_resolver)
    order_resolver.append_and_sort_orders(new_orders)
  
    # SIZE POSITIONS
    position_sizer.run_sizing(positions, quotes)

def select_assets(unviverse_selector: AssetScreener, broker: Broker, data_bundle: DataBundle):
  print(datetime.now(), 'selecting job')
  selection = unviverse_selector.run_screen(data_bundle, broker.get_account_id())
  print(selection)

def _get_start_datetime(start_time: str):
  return f'{date.today()} {start_time}:00'


def run(
  alpha_model: AlphaModel,
  asset_screener: AssetScreener,
  broker: Broker,
  portfolio_opt = EqualPositionSizer(),
  interval: str = '1h',
  start_time: str = '09:30',
  lookback_days: int = 0,
  selection_day: str = 'mon-fri',
  market_data: str = 'tradier',
):
  '''
    selection_interval: https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html?highlight=cron#expression-types
  '''
  data_bundle = DataBundle(broker.account_type)
  scheduler = BlockingScheduler()

  selector_params = (asset_screener, data_bundle, broker)
  scheduler.add_job(select_assets, 'cron', selector_params, day_of_week=selection_day, hour=16, minute=49, timezone='US/Eastern')

  trader_params = (alpha_model, broker, portfolio_opt,
    getattr(data_bundle, market_data),
    data_bundle, start_time, interval, lookback_days)
  scheduler.add_job(trade, 'interval', trader_params, minutes=1, start_date=_get_start_datetime(start_time), timezone='US/Eastern')

  print(scheduler.get_jobs())
  scheduler.start()
