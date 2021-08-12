from datetime import timedelta
from qtsys.broker.broker import Broker
from qtsys.portfolio.equal_portfolio_opt import EqualPorfolioOpt
from qtsys.data.yahoo_data import YahooData


class Engine:
  def __init__(
    self,
    interval: timedelta,
    alpha_model,
    universe_selector,
    broker: Broker,
    portfolio_opt = EqualPorfolioOpt(),
    data_provider = YahooData()
  ):
    self.interval = interval
    self.alpha_model = alpha_model
    self.universe_selector = universe_selector
    self.broker = broker
    self.portfolio_opt = portfolio_opt
    self.data_provider = data_provider
