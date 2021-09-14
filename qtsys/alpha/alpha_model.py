from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd

class AlphaModel(ABC):

  @abstractmethod
  def trade(self, quote, historical_bars, position) -> int:
    pass

  def run_trades(self, symbols: str, quotes: Dict[str, Dict], historical_bars: Dict[str, pd.DataFrame], positions) -> List[str]:
    for symbol in symbols.split(' '):
      signal = self.trade(quotes[symbol], historical_bars[symbol], positions[symbol])
    