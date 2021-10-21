import logging
from datetime import date, datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz

from qtsys.broker.broker import Broker
from qtsys.alpha.alpha_model import AlphaModel
from qtsys.broker.order_resolver import OrderResolver
from qtsys.data.market_data import MarketData
from qtsys.screener.asset_screener import AssetScreener
from qtsys.sizer.position_sizer import PositionSizer
from qtsys.sizer.equal_position_sizer import EqualPositionSizer
from qtsys.data.data_bundle import DataBundle
from qtsys.client import pystorew

logging.basicConfig(format="%(asctime)s %(module)s:%(lineno)d %(message)s", datefmt="%Y-%m-%d %H:%M:%S%z", level=logging.DEBUG)

ny_tz = pytz.timezone('US/Eastern')

def trade(
  alpha_model: AlphaModel,
  broker: Broker,
  position_sizer: PositionSizer,
  data: MarketData,
  interval: str,
  lookback_days: int
):
  logging.info('start trading job')
  if True:
  # if broker.is_market_open():
    today = datetime.now().astimezone(ny_tz).date()
    order_resolver = OrderResolver()
    positions = broker.get_positions()

    # GET ASSETS FROM SCREENER
    symbols = pystorew.read_selection(broker.get_account_id())[str(today)]['selection'].values[0]
    order_resolver.set_closing_orders(symbols, positions)

    # RUN ALPHA MODEL
    quotes = data.get_quotes(symbols)
    start = date.today() - timedelta(days=lookback_days)
    logging.info('downloading %s historical bars', interval)
    historical_bars = data.download_bars(symbols, str(start), str(today), interval)
    logging.info('successfully downloaded %s historical bars', interval)
    new_orders = alpha_model.run_trades(symbols, quotes, historical_bars, positions)
    order_resolver.append_and_sort_orders(new_orders)

    # SIZE POSITIONS
    opening_orders = order_resolver.get_opening_orders()
    desired_positions = position_sizer.run_sizing(opening_orders)
    order_resolver.quantify_opening_orders(desired_positions, positions, quotes, broker.get_balance())

    # PLACE ORDERS
    order_resolver.place_orders(broker)

def select_assets(asset_screener: AssetScreener, broker: Broker, data_bundle: DataBundle):
  logging.info('start asset selection job')
  asset_screener.run_screen(data_bundle, broker.get_account_id())
  logging.info('successfully saved selection')

def get_start_datetime(start_time: str):
  return f'{date.today()} 00:00:00'


def run(
  alpha_model: AlphaModel,
  asset_screener: AssetScreener,
  broker: Broker,
  position_sizer: PositionSizer = EqualPositionSizer(),
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

  selector_params = (asset_screener, broker, data_bundle)
  select_assets(*selector_params)
  scheduler.add_job(select_assets, 'cron', selector_params, day_of_week=selection_day, hour=14, minute=49, timezone='US/Eastern')

  trader_params = (alpha_model, broker, position_sizer, getattr(data_bundle, market_data), interval, lookback_days)
  scheduler.add_job(trade, 'interval', trader_params, minutes=1, start_date=get_start_datetime(start_time), timezone='US/Eastern')

  print(scheduler.get_jobs())
  scheduler.start()
