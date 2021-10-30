from abc import ABC, abstractmethod
from typing import DefaultDict, Dict, List
import pandas as pd
from qtsys.broker.typing import SideOfOrder
from qtsys.broker.order_resolver import Order
from qtsys.broker.position import Position
from qtsys.data.quote import Quote

class AlphaModel(ABC):

  '''
    position: positive if a long position, negative if short position, or 0 if no position.
    returns OrderType
  '''
  @abstractmethod
  def trade(self, quote: Quote, historical_bars, position: Position) -> SideOfOrder:
    pass

  def run_trades(self,
    symbols: str,
    quotes: Dict[str, Quote],
    historical_bars: Dict[str, pd.DataFrame],
    positions: DefaultDict[str, Position]
  ) -> List[Order]:
    orders: List[Order] = []
    for symbol in symbols.split(' '):
      position = positions[symbol]
      quote = quotes[symbol]
      position.quote = quote
      side = self.trade(quote, historical_bars[symbol], position)
      orders.append(Order(symbol, side, abs(position.quantity)))
    return orders
