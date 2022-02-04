from qtsys import live_trade
from qtsys.sample.sample_strategy import Alpha1
from qtsys.broker.tradier_broker import TradierBroker
from qtsys.tradier import TradierData
from qtsys.screener.screener1 import Screener1
from qtsys.sample.equal_position_sizer import EvenPortfolioOptimizer

data = TradierData('paper')
live_trade.run(
  Alpha1(),
  Screener1(),
  TradierBroker('paper', 'margin', data),
  EvenPortfolioOptimizer(),
  '1min'
)