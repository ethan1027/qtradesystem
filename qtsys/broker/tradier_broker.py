from collections import defaultdict
import pandas as pd
from qtsys.client.tradier import TradierClient
from qtsys.broker.broker import AccountType, Broker, OrderType, SideOfOrder
from qtsys.data.market_data import MarketData

class TradierBroker(Broker):
  def __init__(self, account_type: AccountType, market_data: MarketData):
    super().__init__(market_data, account_type)
    self.client = TradierClient(trading_mode=True, account_type=account_type)
    self.account_id = self.client.account_id

  def get_account_id(self) -> str:
    return self.account_id

  def get_balance(self) -> float:
    balances = self.client.get(f'/v1/accounts/{self.account_id}/balances')
    print(balances)
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

  def place_order(self, symbol, side: SideOfOrder, quantity, order_type: OrderType = 'market', limit = None, stop = None):
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

  def is_market_open(self):
    json = self.client.get('/v1/markets/clock').json()
    return json['clock']['state'] == 'open'