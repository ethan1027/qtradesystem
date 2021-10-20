class Position:
  def __init__(self, cost_basis, quantity, symbol):
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