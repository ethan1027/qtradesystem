from qtsys.broker.broker import AccountType
from qtsys.data.tradier_data import TradierData
from qtsys.data.yahoo_data import YahooData
from qtsys.client.iex import IEX

class DataBundle:
  def __init__(self, account_type: AccountType):
    self.tradier = TradierData(account_type)
    self.yahoo = YahooData()
    self.iex = IEX()
