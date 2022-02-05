import logging
from datetime import date, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

from qtsys.broker import Broker
from qtsys.order_resolver import OrderResolver
from qtsys.data import MarketData
from qtsys.util import get_market_today, get_start_datetime

logging.basicConfig(format="%(asctime)s %(module)s:%(lineno)d %(message)s", datefmt="%Y-%m-%d %H:%M:%S%z", level=logging.DEBUG)



def trade(broker: Broker, data: MarketData, interval: str, lookback_days: int):
  logging.info('start trading job')
  if broker.is_market_open():
    today = get_market_today()
    order_resolver = OrderResolver()
    positions = broker.get_positions()

    # GET ASSETS FROM SCREENER
    # symbols = pystorew.read_latest_selection(broker.get_account_id())
    order_resolver.set_closing_orders(symbols, positions)

    # RUN ALPHA MODEL
    quotes = data.get_quotes(symbols)
    start = date.today() - timedelta(days=lookback_days)
    logging.info('downloading %s historical bars', interval)
    historical_bars = data.get_bars(symbols, str(start), str(today), interval)
    logging.info('successfully downloaded %s historical bars', interval)
    new_orders = alpha_model.run_trades(symbols, quotes, historical_bars, positions)
    order_resolver.append_and_sort_orders(new_orders)

    # SIZE POSITIONS
    opening_orders = order_resolver.get_opening_orders()
    desired_positions = position_sizer.apply(opening_orders)
    order_resolver.quantify_opening_orders(desired_positions, positions, quotes, broker.get_balance())

    # PLACE ORDERS
    order_resolver.place_orders(broker)

def select_assets(asset_screener: AssetScreener, broker: Broker, data_bundle: DataBundle):
  logging.info('start asset selection job')
  asset_screener.run_screen(data_bundle, broker.get_account_id())
  logging.info('successfully saved selection')




def run(
  select_assets: AssetSelectionFn,
  construct_portfolio: PortfolioConstructionFn,
  handle_signal: SignalHandler,
  broker: Broker,
  interval: str = '1min',
  start_time: str = '09:30',
  lookback_days: int = 4,
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
  if interval == 'daily':
    scheduler.add_job(trade, 'interval', trader_params, minutes=1440, start_date=get_start_datetime(start_time), timezone='US/Eastern')
  else:
    scheduler.add_job(trade, 'interval', trader_params, minutes=int(interval[:-3]), start_date=get_start_datetime(start_time), timezone='US/Eastern')

  print(scheduler.get_jobs())
  scheduler.start()
