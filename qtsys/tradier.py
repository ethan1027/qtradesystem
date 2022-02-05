import asyncio
from typing import DefaultDict, Dict
import requests
from collections import defaultdict
import logging
from aiohttp import ClientSession
import pandas as pd

from qtsys.config_loader import config
from qtsys.broker import AccountType, BalanceType, Broker, Order, Position
from qtsys.data import MarketData, Quote
from qtsys.util import resample_bar_data


def transform_tradier_quote(quote):
  return Quote(
    quote.get('symbol'),
    quote.get('type'),
    quote.get('last'),
    quote.get('change'),
    quote.get('volume'),
    quote.get('open'),
    quote.get('open'),
    quote.get('close'),
    quote.get('low'),
    quote.get('bid'),
    quote.get('bidsize'),
    quote.get('ask'),
    quote.get('asksize'),
    quote.get('week_52_high'),
    quote.get('week_52_low')
  )

def transform_tradier_position(position, quote: Quote):
  cost_basis = position.get('cost_basis')
  quantity = position.get('quantity')
  symbol = position.get('symbol')
  return Position(cost_basis, int(quantity), symbol, quote)


class TradierClient:
  def __init__(self, trading_mode: bool = False, account_type: AccountType = 'paper'):
    self.url = config['tradier'][account_type]['url']
    self.token = config['tradier'][account_type]['token']
    self.headers = {'Authorization': f'Bearer {self.token}', 'Accept': 'application/json'}
    logging.info('using endpoint %s', self.url)
    if trading_mode:
      logging.info('fetching account profile')
      profile = self.get('/v1/user/profile')
      account_number = profile['profile']['account']['account_number']
      status = profile['profile']['account']['status']
      account_type = profile['profile']['account']['type']
      logging.info('account number: %s', account_number)
      logging.info('account status: %s', status)
      logging.info('account type: %s', account_type)
      self.account_id = account_number

  def get(self, uri, params=None):
    response = requests.get(self.url + uri, params=params, headers=self.headers)
    if response.status_code >= 400:
      print(response.status_code, response.text)
    return response.json()

  def post(self, uri, data):
    response = requests.post(self.url + uri, data, headers=self.headers).json()
    return response

  async def async_get_all(self, loop, uri, params_list):
    async with ClientSession(loop=loop) as session:
      tasks = [asyncio.create_task(self._async_get(session, uri, params)) for params in params_list]
      return await asyncio.gather(*tasks)

  async def _async_get(self, session: ClientSession, uri, params):
    response = await session.get(self.url + uri, params=params, headers=self.headers)
    json = await response.json()
    return (params['symbol'], json)


class TradierData(MarketData):

  _resample_interval = {
    '2min': '1min',
    '30min': '15min',
    '60min': '15min',
  }

  def __init__(self, account_type: AccountType):
    self.client = TradierClient(trading_mode=False, account_type=account_type)

  def get_bars(self, symbols: str, start=None, end=None, interval='60min') -> Dict[str, pd.DataFrame]:
    interval = self._resample_interval[interval] if interval in self._resample_interval else interval
    loop = asyncio.get_event_loop()
    if interval == 'daily':
      params_list = [self._create_data_params(symbol, start, end, interval) for symbol in symbols.split(' ')]
      results = loop.run_until_complete(self.client.async_get_all(loop, '/v1/markets/history', params_list))
      bars_dict = dict(results)
      for symbol, bars in bars_dict.items():
        df = pd.json_normalize(bars['history']['day'])
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
        bars_dict[symbol] = df
      return bars_dict
    else:
      params_list = [self._create_data_params(symbol, f'{start} 09:30', f'{end} 16:00', interval) for symbol in symbols.split(' ')]
      results = loop.run_until_complete(self.client.async_get_all(loop, '/v1/markets/timesales', params_list))
      bars_dict = dict(results)
      for symbol, bars in bars_dict.items():
        df = pd.json_normalize(bars['series']['data'])
        df.set_index('time', inplace=True)
        df.index = pd.to_datetime(df.index)
        if interval in self._resample_interval:
          df = resample_bar_data(df, interval)
        bars_dict[symbol] = df
      return bars_dict

  def _create_data_params(self, symbol, start, end, interval):
    return {'symbol': symbol, 'interval': interval, 'start': start, 'end': end }

  def get_quotes(self, symbols: str) -> Dict[str,Quote]:
    symbols = symbols.replace(' ', ',')
    logging.info('downloading quotes for: %s', symbols)
    quotes = self.client.get('/v1/markets/quotes', { 'symbols': symbols })
    return { quote['symbol']: transform_tradier_quote(quote) for quote in quotes['quotes']['quote'] }


class TradierBroker(Broker):
  def __init__(self, account_type: AccountType, balance_type: BalanceType, market_data: MarketData):
    super().__init__(market_data, account_type, balance_type)
    self.client = TradierClient(trading_mode=True, account_type=account_type)
    self.account_id = self.client.account_id

  def get_balance(self) -> float:
    balances = self.client.get(f'/v1/accounts/{self.account_id}/balances')['balances']
    if self.balance_type == 'margin':
      margin_object = balances.get('pdt', {}) or balances.get('margin', {})
      balance = margin_object.get('day_trade_buying_power', 0)
      logging.info('day trade buying_power %s', balance)
    else:
      balance = balances['total_equity']
    logging.info('balance: %s', balance)
    return balance

  def get_positions(self) -> DefaultDict[str, Position]:
    positions = self.client.get(f'/v1/accounts/{self.account_id}/positions')
    # df = pd.DataFrame(data={''}, index=[pd.Timestamp.now(tz='US/Eastern')])
    if positions['positions'] == 'null':
      return defaultdict(Position)
    position_list = positions['positions']['position']
    symbols = [position['symbol'] for position in position_list]
    quotes = self.market_data.get_quotes(symbols)
    positions_dict = { 
      position['symbol']: transform_tradier_position(position, quotes[position['symbol']]) for position in position_list
    }
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