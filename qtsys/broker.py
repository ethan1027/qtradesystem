from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Literal

from attr import field

from qtsys.data import MarketData
from qtsys.util import get_market_now

SideOfOrder = Literal['buy', 'sell', 'sell_short', 'buy_cover']
OrderType = Literal['market', 'limit', 'stop', 'stop_limit']
AccountType = Literal['live', 'paper']
BalanceType = Literal['cash', 'margin', 'day_margin']

@dataclass
class Order:
  symbol: str
  side: SideOfOrder
  quantity: int
  order_type: OrderType = 'market'
  limit: float = field(default=None)
  stop: float = field(default=None)

  def __str__(self):
    return f'{self.quantity} {self.side} {self.order_type} order {self.symbol}'


@dataclass
class Position:
  symbol: str
  quantity: int
  side: SideOfOrder
  avg_entry_price: float
  current_price: float
  cost_basis: float
  '''average entry price * quantity'''
  unrealized_pl: float
  '''current_price * cost_basis - cost_basis'''

  # def get_cost_basis(self):
  #   return self.avg_entry_price * self.quantity

  # def update_position(self, order: Order, quote: Quote):
  #   '''
  #     only use this for backtest/paper
  #   '''
  #   if order.side == 'buy':
  #     self.avg_entry_price = (self.avg_entry_price * self.quantity) + (quote.last_price * order.quantity)
  #     self.quantity += order.quantity
  #   if order.side == 'sell':
  #     self.quantity -= order.quantity

@dataclass
class Balances:
  cash: float
  buying_power: float
  long_market_value: float
  short_market_value: float
  total_position_value: float
  equity: float
  daytrading_buying_power: float
  timestamp: datetime = field(factory=get_market_now)


class Broker(ABC):
  def __init__(self, market_data: MarketData, account_type: AccountType, balance_type: BalanceType):
    self.market_data = market_data
    self.account_type: AccountType = account_type
    self.balance_type: BalanceType = balance_type

  @abstractmethod
  def account_id(self) -> str:
    pass

  @property
  @abstractmethod
  def balances(self) -> float:
    pass

  @property
  @abstractmethod
  def positions(self) -> Dict[str, Position]:
    pass

  @property
  @abstractmethod
  def orders(self) -> List[Order]:
    pass

  @abstractmethod
  def is_market_open(self):
    pass

  @abstractmethod
  def place_order(self, order: Order):
    pass
