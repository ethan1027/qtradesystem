from datetime import datetime
from qtsys.broker.backtest_broker import BacktestBroker
from qtsys.portfolio.equal_portfolio_opt import EqualPorfolioOpt
from qtsys.data.yahoo_data import YahooData
from qtsys.engine.engine import Engine


class BacktestEngine(Engine):
  def __init__(self,
    start_dt,
    end_dt,
    interval,
    alpha_model,
    universe_selector,
    portfolio_opt = EqualPorfolioOpt(),
    initial_cap = 10000,
    data_provider = YahooData()
  ):
    super().__init__(interval, alpha_model, universe_selector, BacktestBroker(initial_cap), portfolio_opt, data_provider)
    self.start_dt = start_dt
    self.end_dt = end_dt

  def run(self):
    cur_date = datetime.strptime(self.start_dt, '')