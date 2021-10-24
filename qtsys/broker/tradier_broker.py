from collections import defaultdict
from typing import DefaultDict
import pandas as pd
from qtsys.broker.order import Order
from qtsys.broker.position import Position
from qtsys.client.tradier import TradierClient
from qtsys.broker.broker import Broker
from qtsys.broker.typing import AccountType, BalanceType
from qtsys.data.market_data import MarketData

class TradierBroker(Broker):
  def __init__(self, account_type: AccountType, balance_type: BalanceType, market_data: MarketData):
    super().__init__(market_data, account_type, balance_type)
    self.client = TradierClient(trading_mode=True, account_type=account_type)
    self.account_id = self.client.account_id

  def get_account_id(self) -> str:
    return self.account_id

  def get_balance(self) -> float:
    balances = self.client.get(f'/v1/accounts/{self.account_id}/balances')['balances']
    print(balances)
    if self.balance_type == 'margin':
      stock_buying_power = max(balances.get('pdt', {}).get('stock_buying_power', 0), balances.get('margin', {}).get('stock_buying_power', 0))
      balance = stock_buying_power + balances['stock_long_value']
    else:
      balance = balances['total_equity']
    df = pd.DataFrame(data={'balance': [balance]}, index=[pd.Timestamp.now(tz='US/Eastern')])
    print(df)
    return balance

  def get_positions(self) -> DefaultDict[str, Position]:
    positions = self.client.get(f'/v1/accounts/{self.account_id}/positions')
    # df = pd.DataFrame(data={''}, index=[pd.Timestamp.now(tz='US/Eastern')])
    if positions['positions'] == 'null':
      return defaultdict(Position)
    positions_dict = { position['symbol']: Position.from_tradier_position(position) for position in positions['positions']['position'] }
    return defaultdict(Position, positions_dict)

  def get_orders(self):
    orders = self.client.get(f'/v1/accounts/{self.account_id}/orders')
    return orders

  def get_gain_loss(self, symbol: str):
    params = { 'symbol': symbol }
    gainloss = self.client.get(f'/v1/accounts/{self.account_id}/gainloss', params)
    return gainloss['gainloss']['closed_position'][0]

  def place_order(self, order: Order):
    data = {
      'class': 'equity',
      'symbol': order.symbol,
      'side': order.side,
      'quantity': str(order.quantity),
      'type': order.order_type,
      'duration': 'day',
      'limit': '{:.2f}'.format(order.limit) if order.limit else '',
      'stop': '{:.2f}'.format(order.stop) if order.stop else '',
    }
    order = self.client.post(f'/v1/accounts/{self.account_id}/orders', data)
    print('placing order:', order)
    return order

  def is_market_open(self):
    json = self.client.get('/v1/markets/clock').json()
    return json['clock']['state'] == 'open'
