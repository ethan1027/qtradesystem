from qtsys.data.yahoo_data import YahooData
from qtsys.data.tradier_data import TradierData


def run(data_provider):
  if data_provider == 'tradier':
    data = TradierData()
  elif data_provider == 'yahoo':
    data = YahooData()
  
  