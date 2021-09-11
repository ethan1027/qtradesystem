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

  @abstractmethod
  def id(self):
    pass
