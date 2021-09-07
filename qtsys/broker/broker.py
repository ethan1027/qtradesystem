from abc import ABC, abstractmethod

class Broker(ABC):
  @abstractmethod
  def get_balances(self):
    pass

  @abstractmethod
  def get_positions(self):
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

class Position:
  def __init__(self, symbol, cost_basis, date_acquired, quantity, tid):
    self.symbol = symbol
    self.cost_basis = cost_basis
    self.date_acquired = date_acquired
    self.quantity = quantity
    self.tid = tid