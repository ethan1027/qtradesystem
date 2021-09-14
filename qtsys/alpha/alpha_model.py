from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd

class AlphaModel(ABC):

  @abstractmethod
  def trade(self, quote, historical_bars, position) -> int:
    pass

  def run_trades(self, symbols: str, quotes: Dict[str, Dict], historical_bars: Dict[str, pd.DataFrame], positions) -> str:
    for symbol in symbols.split(' '):
      self.trade(quotes[symbol], historical_bars[symbol], positions[symbol])
    