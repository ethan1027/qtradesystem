from abc import ABC, abstractmethod

class Portfolio(ABC):
  @abstractmethod
  def get_balance():
    raise NotImplementedError('should implement get_balance')
  @abstractmethod
  def get_positions():
    pass

  @abstractmethod
  def get_orders():
    pass