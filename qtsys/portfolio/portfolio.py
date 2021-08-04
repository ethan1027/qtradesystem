from abc import ABC, abstractmethod

class Portfolio(ABC):
  @abstractmethod
  def get_balance():
    pass
  
  @abstractmethod
  def get_positions():
    pass

  @abstractmethod
  def get_orders():
    pass