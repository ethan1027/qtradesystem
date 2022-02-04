from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import DefaultDict, Literal, Union

from qtsys.data import MarketData, Quote

SideOfOrder = Literal['buy', 'sell', 'sell_short', 'buy_cover']
OrderType = Literal['market', 'limit', 'stop', 'stop_limit']
AccountType = Literal['live', 'paper']
BalanceType = Literal['cash', 'margin', 'day_margin']


@dataclass
class Position:
  cost_basis: float = 0
  quantity: int = 0
  symbol: str = ''
  quote: Union[Quote, None] = None

  def get_profit_percentage(self):
    if not self.quote:
      return 0
    return self.get_profit_dollar() / (self.cost_basis * abs(self.quantity))

  def get_profit_dollar(self):
    if not self.quote:
      return 0
    return (self.quote.last_price - self.cost_basis) * abs(self.quantity)


@dataclass
class Order:
  symbol: str
  side: SideOfOrder
  quantity: int
  order_type: OrderType = 'market'
  limit: Union[float, None] = None
  stop: Union[float, None] = None

  def __str__(self):
    return f'{self.quantity} {self.side} {self.order_type} order {self.symbol}'


class Broker(ABC):
  def __init__(self, market_data: MarketData, account_type: AccountType, balance_type: BalanceType):
    self.market_data = market_data
    self.account_type: AccountType = account_type
    self.balance_type: BalanceType = balance_type

  @abstractmethod
  def get_account_id(self) -> str:
    pass

  @abstractmethod
  def get_balance(self) -> float:
    pass

  @abstractmethod
  def get_positions(self) -> DefaultDict[str, Position]:
    pass

  @abstractmethod
  def is_market_open(self):
    pass

  @abstractmethod
  def place_order(self, order: Order):
    pass


class BacktestBroker(Broker):
  def __init__(self, market_data: MarketData, balance_type: BalanceType, start_date, initial_cap: int = 10000):
    super().__init__(market_data, 'paper', balance_type)
    self.balance_history = {
      "date": [start_date],
      "balance": [initial_cap],
    }

  def get_account_id(self) -> str:
      return 'backtest_account'

  def get_balance(self):
    return self.balance_history["balance"][-1]

  def get_positions(self):
    pass

  def get_orders(self):
    pass

  def place_order(self, order: Order):
    pass


  def is_market_open(self):
      return True
