from typing import List, Tuple


class OrderResolver:
  def __init__(self, sell_orders: List[Tuple[str, int]] = [], buy_orders: List[Tuple[str, int]] = []):
    self.sell_orders = sell_orders
    self.buy_orders = buy_orders
