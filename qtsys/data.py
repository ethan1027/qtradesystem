from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
import pandas as pd

@dataclass(frozen=True)
class Quote:
  symbol: str
  open_price: float
  high_price: float
  low_price: float
  close_price: float
  last_price: float
  volume: int
  asset_type: str = ''
  change: float = 0
  bid: float = 0
  bid_size: int = 0
  ask: float = 0
  ask_size: int = 0
  week_52_high: float = 0
  week_52_low: float = 0


class MarketData(ABC):
  @abstractmethod
  def get_bars(self, symbols, start, end, interval) -> Dict[str, pd.DataFrame]:
    pass

  @abstractmethod
  def get_quotes(self, symbols: str) -> Dict[str, Quote]:
    pass
