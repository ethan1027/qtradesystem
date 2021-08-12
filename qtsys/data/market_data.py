from abc import ABC, abstractmethod


class MarketData(ABC):

  @abstractmethod
  def download_bars(self):
    raise NotImplementedError('implement download_bars()')
  
  # @abstractmethod
  # def get_bars(cur_date: str, look_back_period):
  #   pass