from typing import DefaultDict, Dict, List

from qtsys.broker.broker import OrderType, SideOfOrder, Broker
from qtsys.data.market_data import Quote


class Order:
  def __init__(self, symbol: str, side: SideOfOrder, quantity: int, order_type: OrderType = 'market', limit = None, stop = None):
    self.symbol = symbol
    self.side = side
    self.quantity = quantity
    self.order_type = order_type
    self.limit = limit
    self.stop = stop

  def to_tuple(self):
    return (self.symbol, self.side, self.quantity, self.order_type, self.limit, self.stop)


class OrderResolver:
  def __init__(self):
    self.orders: List[Order] = []

  def set_closing_orders(self, selected_assets: List[str], positions: DefaultDict[str, int]):
    for symbol, quantity in positions.items():
      if symbol not in selected_assets:
        if quantity > 0:
          self.orders.append(Order(symbol, 'sell', quantity))
        elif quantity < 0:
          self.orders.append(Order(symbol, 'buy_cover', quantity))

  def append_and_sort_orders(self, orders: List[Order]):
    for order in orders:
      if order.side in ('sell', 'buy_cover'):
        self.orders = [order, *self.orders]
      else:
        self.orders.append(order)

  def get_opening_orders(self) -> List[str]:
    return [order.symbol for order in self.orders if order.side in ('buy', 'sell_short')]

  def quantify_opening_orders(self, desired_positions: Dict[str, float], existing_positions: Dict[str, int], quotes: Dict[str, Quote], balance: float):
    for order in self.orders:
      symbol = order.symbol
      percent = desired_positions.get(symbol)
      if percent:
        side_coefficient = { 'buy': 1, 'sell_short': 2 }
        desired_quantity = int(balance * percent // quotes[symbol].last // side_coefficient[order.side])
        existing_quantity = existing_positions[symbol]
        quantity_diff = desired_quantity - existing_quantity
        print(f'adjusting {existing_quantity} {symbol} position by {quantity_diff}')
        order.quantity = abs(quantity_diff)
        if order.side == 'buy':
          order.side = 'sell'
        elif order.side == 'sell_short':
          order.side = 'buy_cover'

  def place_orders(self, broker: Broker):
    for order in self.orders:
      if order.quantity > 0:
        broker.place_order(*order.to_tuple())