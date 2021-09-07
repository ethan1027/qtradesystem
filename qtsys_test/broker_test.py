from qtsys.broker.tradier_broker import TradierBroker

def test_backtest_broker():
  # BacktestBroker()
  pass


def test_tradier_broker():
  broker = TradierBroker(account_type='live')
  print(broker.get_balances())
  print(broker.buy('AAPL', 1))
  