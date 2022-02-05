from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import DefaultDict, Literal, Union

from attr import field

from qtsys.data import MarketData, Quote

SideOfOrder = Literal['buy', 'sell', 'sell_short', 'buy_cover']
OrderType = Literal['market', 'limit', 'stop', 'stop_limit']
AccountType = Literal['live', 'paper']
BalanceType = Literal['cash', 'margin', 'day_margin']


@dataclass
class Position:
  symbol: str = ''
  open_price: float = 0
  close_price: float = 0
  quantity: int = 0
  open_date: datetime = field(default=None)
  close_date: datetime = field(default=None)

  def get_profit_percentage(self, quote: Quote):
    if not self.quantity:
      return 0
    return self.get_profit_dollar(quote) / (self.open_price * abs(self.quantity))

  def get_profit_dollar(self, quote: Quote):
    if not self.quantity:
      return 0
    return (quote.last_price - self.open_price) * abs(self.quantity)



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

