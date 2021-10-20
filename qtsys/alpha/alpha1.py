from qtsys.alpha.alpha_model import AlphaModel
from qtsys.broker.broker import SideOfOrder


class Alpha1(AlphaModel):
  def trade(self, quote, historical_bars, position) -> SideOfOrder:
    return 'buy'
