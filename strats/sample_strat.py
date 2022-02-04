from qtsys.backtest import run_backtest
from qtsys.data import MarketData

def static_portfolio():
  return ['AAPL']

def even_portfolio():
  return { 'AAPL': 0.9}
run_backtest('2021-01-25', static_portfolio, even_portfolio, TradierData())