from qtsys.data.quote import Quote


class Position:
  def __init__(self, cost_basis = 0, quantity = 0, symbol = ''):
    self.cost_basis: float = cost_basis
    self.quantity: int = quantity
    self.symbol: str = symbol

  @staticmethod
  def from_tradier_position(position):
    cost_basis = position.get('cost_basis')
    quantity = position.get('quantity')
    symbol = position.get('symbol')
    return Position(cost_basis, int(quantity), symbol)

  def __int__(self):
    return self.quantity

  @property
  def quote(self) -> Quote:
    return self._quote

  @quote.setter
  def quote(self, value: Quote):
    self._quote = value
  def get_profit_percentage(self):
    return self.get_profit_dollar() / (self.cost_basis * self.quantity)

  def get_profit_dollar(self):
    return (self.quote.last - self.cost_basis) * self.quantity
