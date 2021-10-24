from abc import ABC, abstractmethod
from typing import DefaultDict
from qtsys.broker.typing import AccountType, BalanceType
from qtsys.broker.order import Order
from qtsys.broker.position import Position

from qtsys.data.market_data import MarketData

'''
  Abstract Broker for both backtest and live
'''
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
