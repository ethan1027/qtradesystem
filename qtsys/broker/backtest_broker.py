import pandas as pd
from qtsys.broker.broker import Broker


class BacktestBroker(Broker):
  def __init__(self, initial_cap, start_date):
    self.events = pd.DataFrame(columns=[], index='date')
    self.portfolio = pd.DataFrame([[initial_cap]], columns=['capital'], index=[pd.to_datetime(start_date)])
    self.positions = []
  
  def get_balances(self):
    pass

  def get_positions(self):
    pass
    
  def get_orders(self):
    pass

  def buy(self, symbol, quantity, order_type = 'market', limit = None, stop = None):
    pass

  def sell(self, symbol, quantity, order_type = 'market', limit = None, stop = None):
    pass

  def sell_short(self, symbol, quantity, order_type):
    pass