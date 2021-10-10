from collections import defaultdict
import pandas as pd
from qtsys.client.tradier import TradierClient
from qtsys.broker.broker import AccountType, Broker
from qtsys.data.market_data import MarketData

class TradierBroker(Broker):
  def __init__(self, account_type: AccountType, market_data: MarketData):
    super().__init__(market_data)
    self.client = TradierClient(trading_mode=True, account_type=account_type)
    self.account_id = self.client.account_id

  def get_account_id(self) -> str:
    return self.account_id

  def get_balances(self) -> float:
    balances = self.client.get(f'/v1/accounts/{self.account_id}/balances')
    total_equity = balances['balances']['total_equity']
    df = pd.DataFrame(data={'total_equity': [total_equity]}, index=[pd.Timestamp.now(tz='US/Eastern')])
    print(df)
    return total_equity

  def get_positions(self):
    positions = self.client.get(f'/v1/accounts/{self.account_id}/positions')
    # df = pd.DataFrame(data={''}, index=[pd.Timestamp.now(tz='US/Eastern')])
    return defaultdict(int, { position['symbol']: position for position in positions['positions']['position']})

  def get_orders(self):
    orders = self.client.get(f'/v1/accounts/{self.account_id}/orders')
    return orders

  def get_gain_loss(self, symbol: str):
    params = { 'symbol': symbol }
    gainloss = self.client.get(f'/v1/accounts/{self.account_id}/gainloss', params)
    return gainloss['gainloss']['closed_position'][0]

  def place_order(self, symbol, side, quantity, order_type = 'market', limit = None, stop = None):
    data = {
      'class': 'equity',
      'symbol': symbol,
      'side': side,
      'quantity': str(quantity),
      'type': order_type,
      'duration': 'day',
      'limit': '{:.2f}'.format(limit) if limit else '',
      'stop': '{:.2f}'.format(stop) if stop else '',
    }
    order = self.client.post(f'/v1/accounts/{self.account_id}/orders', data)
    print('placing order:', order)
    return order

  def buy(self, symbol, quantity, order_type = 'market', limit = None, stop = None):
    return self.place_order(symbol, 'buy', quantity, order_type, limit, stop)

  def sell(self, symbol, quantity, order_type = 'market', limit = None, stop = None):
    order = self.place_order(symbol, 'sell', quantity, order_type, limit, stop)
    gainloss = self.get_gain_loss(symbol)
    print(gainloss)
    return order


  def buy_to_cover(self):
    pass

  def sell_short(self):
    pass

  def is_market_open(self):
    json = self.client.get('/v1/markets/clock').json()
    return json['clock']['state'] == 'open'