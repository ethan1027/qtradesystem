from typing import DefaultDict, Literal
from abc import ABC, abstractmethod

from qtsys.data.market_data import MarketData


SideOfOrder = Literal['buy', 'sell', 'sell_short', 'buy_cover']
OrderType = Literal['market', 'limit', 'stop', 'stop_limit']
AccountType = Literal['live', 'paper']
BalanceType = Literal['cash', 'margin', 'day_margin']

'''
  Abstract Broker for both backtest and live
'''
class Broker(ABC):
  def __init__(self, market_data: MarketData, account_type: AccountType, balance_type: BalanceType):
    self.market_data = market_data
    self.account_type: AccountType = account_type
    self.balance_type: BalanceType = balance_type

  @abstractmethod
  def get_account_id(self) -> str:
    pass

  @abstractmethod
  def get_balance(self) -> float:
    pass

  @abstractmethod
  def get_positions(self) -> DefaultDict[str, int]:
    pass

  @abstractmethod
  def is_market_open(self):
    pass

  @abstractmethod
  def place_order(self, symbol, side: SideOfOrder, quantity, order_type: OrderType, limit, stop):
    pass

  # def resolve_orders_quantity(self, portfolio_target: Dict[str, float]) -> None:
  #   symbols = ','.join(portfolio_target.keys())
  #   balance = self.get_balances()
  #   quotes = self.market_data.get_quotes(symbols)
  #   position_target = {}
  #   for symbol, percentage in portfolio_target.items():
  #     position_target[symbol] = balance * percentage // quotes[symbol]['last']
  #   current_positions = self.get_positions()
  #   order_target = Counter(position_target) - Counter(current_positions)
  #   order_resolver = OrderResolver()
  #   for symbol, quantity in order_target.most_common():
  #     if quantity > 0:
  #       order_resolver.buy_orders.append((symbol, quantity))
  #     elif quantity < 0:
  #       order_resolver.sell_orders.append((symbol, abs(quantity)))
  #   return None 

  # def resolve_orders(self, porfolio_target: Dict[str, float]):
  #   order_resolver = self.resolve_orders_quantity(porfolio_target)
  #   for symbol, quantity in order_resolver.sell_orders:
  #     self.sell(symbol, quantity)
  #   for symbol, quantity in order_resolver.buy_orders:
  #     quotes = self.market_data.get_quotes(symbol)
  #     self.buy(symbol, quantity)