from qtsys.data.yahoo_data import YahooData
from qtsys.engine.engine import Engine


class BacktestEngine(Engine):
  def __init__(self,
    start_dt,
    end_dt,
    alpha_model,
    universe_selector,
    portfolio_optimizer = EqualPorfolioOptimizer(),
    initial_cash = 10000,
    data_provider = YahooData()
  ):
    self.start_dt = start_dt
    self.end_dt = end_dt

  def run(self):
   pass 