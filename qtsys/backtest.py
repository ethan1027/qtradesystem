from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import DefaultDict, Dict
import pandas as pd
import pandas_market_calendars as mcal
from qtsys.steps import AssetSelectionFn, PortfolioConstructionFn, SignalHandlerFn, run_asset_selection, run_portfolio_construction
from qtsys.broker import BalanceType, Broker, Order, Position
from qtsys.data import MarketData, Quote


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
  initial_capital = 10000,
  lookback_days = 30,
  signal_symbols: str = 'SPY',
):
  broker = BacktestBroker(market_data, 'cash', start_dt, initial_capital)
  print('input', start_dt, end_dt)
  nyse = mcal.get_calendar('NYSE')
  schedule = nyse.schedule(start_dt, end_dt)
  print(schedule)
  print()

  portfolio_day_counter = 0
  portfolio_timeline = {
    'date': [],
    'portfolio': []
  }
  accumulative_portfolio = set()

  portfolio_target = {}
  for _, row in schedule.iterrows():
    selection_time = (row['market_open']).astimezone(nyse.tz.zone)
    if portfolio_day_counter % portfolio_interval.days == 0:
      portfolio_symbols = run_asset_selection(construct_portfolio, market_data)
      portfolio_target = run_portfolio_construction(optimize_portfolio, portfolio_symbols, broker.get_positions())
      print('selecting', selection_time, portfolio_target)
      accumulative_portfolio.update(portfolio_symbols)
    portfolio_timeline['date'].append(selection_time)
    portfolio_timeline['portfolio'].append(portfolio_target)

  print('accumulative portfolio', accumulative_portfolio)
  print()

  for _, row in schedule.iterrows():
    trading_time = (row['market_open']).astimezone(nyse.tz.zone) + offset
    while trading_time < row['market_close']:
      # strategy.apply(portfolio_symbols)
      print('trading', trading_time)
      trading_time += interval



class BacktestBroker(Broker):
  def __init__(self, market_data: MarketData, balance_type: BalanceType, start_date, initial_cap: int = 10000):
    super().__init__(market_data, 'paper', balance_type)
    self.balance = initial_cap
    self.positions = defaultdict(Position)
    self.balance_history = {
      'date': [start_date],
      'balance': [initial_cap],
    }

  def get_account_id(self) -> str:
      return 'backtest_account'

  def get_balance(self):
    return self.balance_history["balance"][-1]

  def get_positions(self) -> DefaultDict[str, Position]:
    return self.positions

  def get_orders(self):
    pass

  def place_order(self, order: Order):
    pass

  def is_market_open(self):
      return True


@dataclass
class BacktestMarketData(MarketData):
  historical_data_dict: Dict[str, pd.DataFrame]
  sim_end: datetime
  lookback_days: int

  def get_bars(self, symbols, start, end, interval) -> Dict[str, pd.DataFrame]:
    sim_start = self.sim_end - timedelta(days=self.lookback_days)
    return {
      symbol: df[sim_start:self.sim_end,:] for symbol, df in self.historical_data_dict.items()
    }

  def get_quotes(self, symbols: str) -> Dict[str, Quote]:
    return {
      symbol: self._df_to_quote(symbol) for symbol in symbols.split(' ')
    }

  def _df_to_quote(self, symbol: str) -> Quote:
    row = self.historical_data_dict[symbol][self.sim_end]
    # TODO
    print('quote', row)
    return Quote(
      symbol,
      0,
      0,
      0,
      0,
      0,
      0
    )
  