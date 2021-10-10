from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd


class MarketData(ABC):

  @abstractmethod
  def download_bars(self, symbols, start, end, interval) -> Dict[str, pd.DataFrame]:
    pass

  @abstractmethod
  def get_historical_bars(self, symbols, current_date):
    pass

  @abstractmethod
  def get_quotes(self, symbols) -> Dict[str, Dict]:
    pass

