from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd
from qtsys.broker.broker import SideOfOrder
from qtsys.broker.order_resolver import Order, OrderResolver

class AlphaModel(ABC):

  '''
    position: positive if a long position, negative if short position, or 0 if no position.
    returns OrderType
  '''
  @abstractmethod
  def trade(self, quote, historical_bars, position: int) -> SideOfOrder:
    pass

  def run_trades(self, symbols: str, quotes: Dict[str, Dict], historical_bars: Dict[str, pd.DataFrame], positions, order_resolver: OrderResolver) -> None:
    for symbol in symbols.split(' '):
      position = positions[symbol]
      side_of_order = self.trade(quotes[symbol], historical_bars[symbol], position)
      )