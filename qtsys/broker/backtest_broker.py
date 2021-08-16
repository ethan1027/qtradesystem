import pandas as pd
import numpy as np
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

  def buy(self, symbol, quantity, type):
    pass

  def sell(self, symbol, quantity, type):
    pass

  def sell_short(self, symbol, quantity, type):
    pass