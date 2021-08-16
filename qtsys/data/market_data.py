from abc import ABC, abstractmethod


class MarketData(ABC):

  @abstractmethod
  def download_bars(self):
    pass
  
  @abstractmethod
  def get_historical_bars(self):
    pass