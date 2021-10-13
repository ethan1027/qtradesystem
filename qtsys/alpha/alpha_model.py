from abc import ABC, abstractmethod
from typing import DefaultDict, Dict, List
import pandas as pd
from qtsys.broker.broker import SideOfOrder
from qtsys.broker.order_resolver import Order
from qtsys.data.market_data import Quote

class AlphaModel(ABC):

  '''
    position: positive if a long position, negative if short position, or 0 if no position.
    returns OrderType
  '''
  @abstractmethod
  def trade(self, quote, historical_bars, position: int) -> SideOfOrder:
    pass

  def run_trades(self,
    symbols: str,
    quotes: Dict[str, Quote],
    historical_bars: Dict[str, pd.DataFrame],
    positions: DefaultDict[str, int]
  ) -> List[Order]:
    orders: List[Order] = []
    for symbol in symbols.split(' '):
      side = self.trade(quotes[symbol], historical_bars[symbol], positions[symbol])
      orders.append(Order(symbol, side, abs(positions[symbol])))
    return orders