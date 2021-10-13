from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd

class Quote:
  def __init__(self, quote):
    self.symbol: str = quote.get('symbol')
    self.type: str = quote.get('type')
    self.last: float = quote.get('last')
    self.change: float = quote.get('change')
    self.volume: int = quote.get('volume')
    self.open: float = quote.get('open')
    self.high: float = quote.get('high')
    self.low: float = quote.get('low')
    self.bid: float = quote.get('bid')
    self.bid_size: int = quote.get('bid_size')
    self.ask: float = quote.get('ask')
    self.ask_size: int = quote.get('ask_size')
    self.week_52_high: float = quote.get('week_52_high')
    self.week_52_low: float = quote.get('week_52_low')


class MarketData(ABC):

  @abstractmethod
  def download_bars(self, symbols, start, end, interval) -> Dict[str, pd.DataFrame]:
    pass

  @abstractmethod
  def get_historical_bars(self, symbols, current_date):
    pass

  @abstractmethod
  def get_quotes(self, symbols) -> Dict[str, Quote]:
    pass


