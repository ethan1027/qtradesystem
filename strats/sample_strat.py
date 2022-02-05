from qtsys.backtest import run_backtest
from qtsys.tradier import TradierData

def static_portfolio(a):
  return ['AAPL']

def even_portfolio(a):
  return { 'AAPL': 0.9}

def buy_and_hold(a, b, c):
  return 'buy'

run_backtest('2022-01-25', static_portfolio, even_portfolio, buy_and_hold, TradierData('paper'))