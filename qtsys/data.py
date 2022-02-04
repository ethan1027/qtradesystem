from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
import pandas as pd

@dataclass
class Quote:
  symbol: str
  asset_type: str
  open_price: float
  close_price: float
  high_price: float
  low_price: float
  last_price: float
  change: float
  volume: int
  bid: float
  bid_size: int
  ask: float
  ask_size: int
  week_52_high: float
  week_52_low: float


class MarketData(ABC):
  @abstractmethod
  def get_bars(self, symbols, start, end, interval) -> Dict[str, pd.DataFrame]:
    pass

  @abstractmethod
  def get_quotes(self, symbols) -> Dict[str, Quote]:
    pass
