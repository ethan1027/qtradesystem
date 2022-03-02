from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from turtle import position
from typing import DefaultDict, Dict
import pandas as pd
import pandas_market_calendars as mcal
from qtsys.steps import AssetSelectionFn, PortfolioConstructionFn, SignalHandlerFn, run_asset_selection, run_portfolio_construction
from qtsys.broker import BalanceType, Balances, Broker, Order, Position
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
  print('input', start_dt, end_dt)
  nyse = mcal.get_calendar('NYSE')
  schedule = nyse.schedule(start_dt, end_dt)
  broker = BacktestBroker(market_data, 'cash', schedule[0]['market_open'].astimezone(nyse.tz.zone), initial_capital)
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
      portfolio_target = run_portfolio_construction(optimize_portfolio, portfolio_symbols, broker.positions)
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
  def __init__(self, market_data: MarketData, balance_type: BalanceType, start_date: datetime, initial_cap: int = 10000, enable_margin: boolean = False):
    super().__init__(market_data, 'paper', balance_type)
    margin_buying_power = initial_cap * 2 if enable_margin else 0
    self._balances_history = [Balances(
      cash=initial_cap,
      buying_power=margin_buying_power,
      long_market_value=0,
      short_market_value=0,
      total_position_value=0,
      equity=initial_cap,
      daytrading_buying_power=margin_buying_power,
      timestamp=start_date
    )]
    self._positions: Dict[str, Position] = {}
    self._orders = []

  def account_id(self) -> str:
      return 'backtest_account'

  @property
  def balances(self):
    return self._balances_history[-1]

  @property
  def positions(self) -> Dict[str, Position]:
    return self._positions

  @property
  def orders(self):
    return self._orders

  def place_order(self, order: Order):
    if order.side == 'buy':

    elif order.side == 'sell':
      pass
    elif order.side == 'buy_cover':
      pass
    elif order.side == 'sell_short':
      pass

  def _place_buy_order(self, order: Order):
    quote = self.market_data.get_quotes(order.symbol)[order.symbol]
    prev_position = self.positions.get(order.symbol)
    order_cost_basis = order.quantity + quote.last_price
    if prev_position:
      if prev_position.side == 'buy':
        total_quantity = prev_position.quantity + order.quantity
        new_position = Position(
          symbol=order.symbol,
          quantity=total_quantity,
          side=order.side,
          avg_entry_price=(prev_position.cost_basis + order_cost_basis) / total_quantity,
          current_price=quote.last_price,
          cost_basis=prev_position.cost_basis + order_cost_basis,
          unrealized_pl=prev_position.unrealized_pl)
        self._positions[order.symbol] = new_position

        prev_balances = self._balances_history[-1]
        new_balances = Balances(
          cash=initial_cap,
          buying_power=margin_buying_power,
          long_market_value=0,
          short_market_value=0,
          total_position_value=0,
          equity=initial_cap,
          daytrading_buying_power=margin_buying_power,
          timestamp=start_date
        )

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
    print('quote', row)
    return Quote(symbol, row['open'], row['high'], row['low'], row['close'], row['close'], row['volume'])
  