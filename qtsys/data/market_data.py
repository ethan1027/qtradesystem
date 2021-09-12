from abc import ABC, abstractmethod
from typing import Dict


class MarketData(ABC):

  @abstractmethod
  def download_bars(self, symbols, start, end, interval):
    pass

  @abstractmethod
  def get_historical_bars(self, symbols, current_date):
    pass

  @abstractmethod
  def get_quotes(self, symbols) -> Dict[str, Dict]:
    pass
