from datetime import date, timedelta
import pandas_market_calendars as mcal
from qtsys.base_steps import AssetSelectionFn, PortfolioConstructionFn, SignalHandlerFn, run_asset_selection, run_portfolio_construction
from qtsys.broker import BacktestBroker
from qtsys.data import MarketData


def run_backtest(
  start_dt: str,
  construct_portfolio: AssetSelectionFn,
  optimize_portfolio: PortfolioConstructionFn,
  handle_signal: SignalHandlerFn,
  market_data: MarketData,
  end_dt: str = date.today().strftime("%Y-%m-%d"),
  interval: timedelta = timedelta(minutes=30),
  offset: timedelta = timedelta(minutes=1),
  portfolio_interval: timedelta = timedelta(days=1),
  initial_capital=10000
):
  broker = BacktestBroker(market_data, 'cash', start_dt, initial_capital)
  print('input', start_dt, end_dt)
  nyse = mcal.get_calendar('NYSE')
  schedule = nyse.schedule(start_dt, end_dt)
  print(schedule)
  portfolio_day_interval = portfolio_interval.days
  portfolio_day_counter = 0
  for _, row in schedule.iterrows():
    portfolio_symbols = []
    portfolio_target = {}
    print(row)
    if portfolio_day_counter % portfolio_day_interval == 0:
      portfolio_symbols = run_asset_selection(construct_portfolio, market_data)
      portfolio_target = run_portfolio_construction(optimize_portfolio, portfolio_symbols)
    current_time = (row['market_open'] + offset).astimezone(nyse.tz.zone)
    while current_time < row['market_close']:
      # strategy.apply(portfolio_symbols)
      print('trading', current_time)
      current_time += interval

  for _, row in schedule.iterrows():
    current_time = (row['market_open'] + offset).astimezone(nyse.tz.zone)
    while current_time < row['market_close']:
      # strategy.apply(portfolio_symbols)
      print('trading', current_time)
      current_time += interval

