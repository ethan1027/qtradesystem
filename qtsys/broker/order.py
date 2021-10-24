from qtsys.broker.typing import OrderType, SideOfOrder


class Order:
  def __init__(self, symbol: str, side: SideOfOrder, quantity: int, order_type: OrderType = 'market', limit = None, stop = None):
    self.symbol = symbol
    self.side: SideOfOrder = side
    self.quantity = quantity
    self.order_type: OrderType = order_type
    self.limit = limit
    self.stop = stop

  def __str__(self):
    return f'{self.quantity} {self.side} {self.order_type} order {self.symbol}'
