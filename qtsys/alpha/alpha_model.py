from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd
from qtsys.broker.broker import OrderType

class AlphaModel(ABC):

  '''
    position: positive if a long position, negative if short position, or 0 if no position.
    returns OrderType
  '''
  @abstractmethod
  def trade(self, quote, historical_bars, position: int) -> OrderType:
    pass

  def run_trades(self, symbols: str, quotes: Dict[str, Dict], historical_bars: Dict[str, pd.DataFrame], positions) -> Dict[str,OrderType]:
    symbols_to_order = {}
    for symbol in symbols.split(' '):
        symbols_to_order[symbol] = self.trade(quotes[symbol], historical_bars[symbol], positions[symbol])
    return symbols_to_order
