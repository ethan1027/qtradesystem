from qtsys.broker.broker import OrderType, SideOfOrder


class Order:
  def __init__(self, symbol: str, side: SideOfOrder, quantity: int, order_type: OrderType = 'market', limit = None, stop = None):
    self.symbol = symbol
    self.side: SideOfOrder = side
    self.quantity = quantity
    self.order_type: OrderType = order_type
    self.limit = limit
    self.stop = stop

  def to_tuple(self):
    return (self.symbol, self.side, self.quantity, self.order_type, self.limit, self.stop)

