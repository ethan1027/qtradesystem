import pandas as pd
from qtsys.client.tradier import TradierClient
from qtsys.broker.broker import Broker
import qtsys.client.pystorew as ps


class TradierBroker(Broker):
  def __init__(self, account_type: str = 'paper'):
    self.client = TradierClient(trading_mode=True, account_type=account_type)

  def get_balances(self):
    balances = self.client.get(f'/v1/accounts/{self.client.account_id}/balances')
    total_equity = balances['balances']['total_equity']
    df = pd.DataFrame(data={'total_equity': [total_equity]}, index=[pd.Timestamp.now(tz='US/Eastern')])
    print(df)
    return total_equity

  def get_positions(self):
    positions = self.client.get(f'/v1/accounts/{self.client.account_id}/positions')
    df = pd.DataFrame(data={''}, index=[pd.Timestamp.now(tz='US/Eastern')])
    return positions

  def get_orders(self):
    orders = self.client.get(f'/v1/accounts/{self.client.account_id}/orders')
    return orders

  def place_order(self, symbol, side, quantity, order_type = 'market', limit = None, stop = None, tag = None):
    data = {
      'class': 'equity',
      'symbol': symbol,
      'side': side,
      'quantity': str(quantity),
      'type': order_type,
      'duration': 'day',
      'limit': '{:.2f}'.format(limit) if limit else '',
      'stop': '{:.2f}'.format(stop) if stop else '',
      'tag': tag,
      'preview': 'true'
    }
    preview = self.client.post(f'/v1/accounts/{self.client.account_id}/orders', data)
    print('preview order:', preview)
    if preview['order']['status'] == 'ok':
    return


  def buy(self, symbol, quantity, order_type = 'market', limit = None, stop = None, tag = None):
    return self.place_order(symbol, 'buy', quantity, order_type, limit, stop, tag)

  def sell(self, symbol, quantity, order_type = 'market', limit = None, stop = None, tag = None):
    return self.place_order(symbol, 'sell', quantity, order_type = 'market', limit = None, stop = None, tag = None)

  def sell_short(self):
    pass

  def fulfill_orders(self):
    pass

  def is_market_open(self):
    json = self.client.get('/v1/markets/clock').json()
    return json['clock']['state'] == 'open'
