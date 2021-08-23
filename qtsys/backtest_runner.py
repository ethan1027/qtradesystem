from datetime import date, timedelta
import pandas_market_calendars as mcal
from qtsys.selector.universe_selector import UniverseSelector
from qtsys.alpha.alpha_model import AlphaModel
from qtsys.broker.backtest_broker import BacktestBroker
from qtsys.portfolio.equal_portfolio_opt import EqualPortfolioOpt
from qtsys.data.yahoo_data import YahooData


def run(
  start_dt: str,
  alpha_model: AlphaModel,
  universe_selector: UniverseSelector,
  portfolio_opt=EqualPortfolioOpt(),
  end_dt=date.today().strftime("%Y-%m-%d"),
  interval=timedelta(minutes=30),
  offset=timedelta(minutes=1),
  selection_interval=timedelta(days=1),
  initial_capital=10000,
  trading_data=YahooData()
):
  broker = BacktestBroker(initial_capital, start_dt)
  print('input', start_dt, end_dt)
  nyse = mcal.get_calendar('NYSE')
  schedule = nyse.schedule(start_dt, end_dt)
  print(schedule)
  for _, row in schedule.iterrows():
    current_time = (row['market_open'] + offset).astimezone(nyse.tz.zone)
    while current_time < row['market_close']:
      print('trading', current_time)
      current_time += interval
   


