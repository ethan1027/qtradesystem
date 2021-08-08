from abc import ABC, abstractmethod

class Broker(ABC):
  @abstractmethod
  def get_balance():
    raise NotImplementedError('should implement get_balance')

  @abstractmethod
  def get_positions():
    raise NotImplementedError('should implement get_positions')

  @abstractmethod
  def get_orders():
    pass