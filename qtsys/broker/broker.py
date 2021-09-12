from abc import ABC, abstractmethod
from collections import Counter
from typing import Dict

from qtsys.data.market_data import MarketData

class Broker(ABC):
  def __init__(self, market_data: MarketData):
    self.market_data = market_data

  @abstractmethod
  def get_balances(self) -> float:
    pass

  @abstractmethod
  def get_positions(self) -> Dict[str, int]:
    pass

  @abstractmethod
  def get_orders(self):
    pass

  @abstractmethod
  def buy(self, symbol, quantity, order_type, limit, stop):
    pass

  @abstractmethod
  def sell(self, symbol, quantity, order_type, limit, stop):
    pass
  
  @abstractmethod
  def sell_short(self, symbol, quantity, order_type):
    pass

  @abstractmethod
  def is_market_open(self):
    pass
  
  def resolve_orders_quantity(self, portfolio_target: Dict[str, float]) -> Dict[str, int]:
    symbols = ' '.join(portfolio_target.keys())
    balance = self.get_balances()
    quotes = self.market_data.get_quotes(symbols)
    position_target = {}
    for symbol, percentage in portfolio_target.items():
      position_target[symbol] = balance * percentage // quotes[symbol]['last']
    
    current_positions = self.get_positions()
    return Counter(position_target) - Counter(current_positions)
    

