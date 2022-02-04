from qtsys.broker.tradier_broker import TradierBroker
from qtsys.tradier import TradierData

def test_backtest_broker():
  # BacktestBroker()
  pass


def test_tradier_broker():
  broker = TradierBroker(account_type='live', market_data=TradierData(account_type='live'))
  print(broker.get_balance())