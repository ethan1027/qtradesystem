from datetime import date, timedelta
import pytz
import pandas_market_calendars as mcal
from qtsys.selector.universe_selector import UniverseSelector
from qtsys.alpha.alpha_model import AlphaModel
from qtsys.broker.backtest_broker import BacktestBroker
from qtsys.portfolio.equal_portfolio_opt import EqualPorfolioOpt
from qtsys.data.yahoo_data import YahooData
from qtsys.engine.engine import Engine


class BacktestEngine(Engine):
  def __init__(self,
    alpha_model: AlphaModel,
    universe_selector: UniverseSelector,
    portfolio_opt = EqualPorfolioOpt(),
    initial_cap = 10000,
    data_provider = YahooData()
  ):
    super().__init__(
      alpha_model, 
      universe_selector, 
      # BacktestBroker(initial_cap), 
      None,
      portfolio_opt, 
      data_provider)

  def run(self, 
    start_dt: str,
    end_dt: str = date.today().strftime("%Y-%m-%d"),
    interval: timedelta = timedelta(minutes=30),
    offset: timedelta = timedelta(minutes=15), 
    selection_interval: timedelta = timedelta(days=1)
  ):
    print('input', start_dt, end_dt)
    nyse = mcal.get_calendar('NYSE')
    schedule = nyse.schedule(start_dt, end_dt)
    print(schedule)
    for _, row in schedule.iterrows():
      cur_trading_time = (row['market_open'] + offset).astimezone(nyse.tz.zone)
      while cur_trading_time < row['market_close']:
        print('trading', cur_trading_time)
        cur_trading_time += interval
   

BacktestEngine(None, None).run('2021-08-03')

