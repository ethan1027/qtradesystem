from typing import Callable, DefaultDict, Dict, List
from xmlrpc.client import boolean

import pandas as pd
from qtsys.broker import Order, Position, SideOfOrder

from qtsys.data import MarketData, Quote


AssetSelectionFn = Callable[[MarketData], List[str]]

def run_asset_selection(func: AssetSelectionFn, market_data: MarketData) -> List[str]:
  return func(market_data)

PortfolioConstructionFn = Callable[[List[str]], Dict[str, float]]

def run_portfolio_construction(
  func: PortfolioConstructionFn,
  symbols: List[str],
  positions: DefaultDict[str, Position],
  rebalance: boolean = False) -> Dict[str, float]:
  desired_positions = func(symbols)
  total_allocation = sum(desired_positions.values())
  if total_allocation > 1 or total_allocation < 0:
    raise RuntimeError('total allocation must be between 0 and 1')
  return desired_positions


SignalHandlerFn = Callable[[pd.DataFrame, Position, Quote], SideOfOrder]

def run_handle_signals(
  func: SignalHandlerFn,
  symbols: str,
  historical_bars: Dict[str, pd.DataFrame],
  positions: DefaultDict[str, Position],
  quotes: Dict[str, Quote]
) -> List[Order]:
  orders: List[Order] = []
  for symbol in symbols.split(' '):
    position = positions[symbol]
    side = func(historical_bars[symbol], position,quotes[symbol])
    orders.append(Order(symbol, side, abs(position.quantity)))
  return orders
