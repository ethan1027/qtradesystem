from qtsys.alpha.alpha_model import AlphaModel
from qtsys.broker.position import Position
from qtsys.broker.typing import SideOfOrder
from qtsys.data.quote import Quote
from qtsys.util.time_util import get_market_now


class Alpha1(AlphaModel):
  def trade(self, quote: Quote, historical_bars, position: Position) -> SideOfOrder: 
    now = get_market_now()
    if position.quantity == 0 and now.hour >= 13 and now.minute >= 30:
      return 'buy'
    elif position.quantity >= 0 and (position.get_profit_percentage() < -3.0 or position.get_profit_percentage() > 3.0):
      return 'sell'
    return 'buy'
