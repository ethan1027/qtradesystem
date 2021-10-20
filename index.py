from qtsys import live_runner
from qtsys.alpha.alpha1 import Alpha1
from qtsys.broker.tradier_broker import TradierBroker
from qtsys.data.tradier_data import TradierData
from qtsys.screener.screener1 import Screener1
from qtsys.sizer.equal_position_sizer import EqualPositionSizer

data = TradierData('paper')
live_runner.run(
  Alpha1(),
  Screener1(),
  TradierBroker('paper', 'margin', data),
  EqualPositionSizer(),
  '1m'
)