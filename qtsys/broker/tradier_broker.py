from qtsys.client.tradier import TradierClient
from qtsys.broker.broker import Broker


class TradierBroker(Broker):
  def __init__(self):
    self.client = TradierClient(trading_mode=True)

  def get_balances(self):
    balances = self.client.http_get(f'/v1/accounts/{self.client.account_id}/balances').json()
    return balances
