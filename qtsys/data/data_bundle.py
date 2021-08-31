from qtsys.data.tradier_data import TradierData
from qtsys.data.yahoo_data import YahooData
from qtsys.client.iex import IEX

class DataBundle:
  def __init__(self):
    self.tradier = TradierData()
    self.yahoo = YahooData()
    self.iex = IEX()