from typing import DefaultDict, Dict, List
import logging

from qtsys.broker import Broker, Order, Position
from qtsys.data import Quote



class OrderResolver:
  def __init__(self):
    self.orders: List[Order] = []

  def set_closing_orders(self, selected_assets: List[str], positions: DefaultDict[str, Position]):
    for symbol, position in positions.items():
      quantity = position.quantity
      if symbol not in selected_assets:
        logging.info('closing position %s %s', quantity, symbol)
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

  def quantify_opening_orders(self, desired_positions: Dict[str, float], existing_positions: Dict[str, Position], quotes: Dict[str, Quote], balance: float):
    for order in self.orders:
      symbol = order.symbol
      percent = desired_positions.get(symbol)
      if percent:
        side_coefficient = { 'buy': 1, 'sell_short': -2 }
        quote = quotes[symbol].ask
        desired_quantity = int(balance * percent // quote // side_coefficient[order.side])
        existing_quantity = existing_positions[symbol].quantity
        quantity_diff = desired_quantity - existing_quantity
        logging.info('%s - %s = %s %s order', desired_quantity, existing_quantity, quantity_diff, symbol)
        order.quantity = abs(quantity_diff)
        if order.side == 'buy' and quantity_diff < 0:
          order.side = 'sell'
        elif order.side == 'sell_short' and quantity_diff > 0:
          order.side = 'buy_cover'

  def place_orders(self, broker: Broker):
    for order in self.orders:
      if order.quantity > 0:
        logging.info('placing %s', order)
        broker.place_order(order)
