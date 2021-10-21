import asyncio
import logging
from aiohttp import ClientSession
import requests
from qtsys.global_config import global_config
from qtsys.broker.broker import AccountType



class TradierClient:
  def __init__(self, trading_mode: bool = False, account_type: AccountType = 'paper'):
    self.url = global_config['tradier'][account_type]['url']
    self.token = global_config['tradier'][account_type]['token']
    self.headers = {'Authorization': f'Bearer {self.token}', 'Accept': 'application/json'}
    logging.info('using endpoint %s', self.url)
    if trading_mode:
      logging.info('fetching account profile')
      profile = self.get('/v1/user/profile')
      account_number = profile['profile']['account']['account_number']
      status = profile['profile']['account']['status']
      type = profile['profile']['account']['type']
      logging.info('account number: %s', account_number)
      logging.info('account status: %s', status)
      logging.info('account type: %s', type)
      self.account_id = account_number

  def get(self, uri, params=None):
    response = requests.get(self.url + uri, params=params, headers=self.headers)
    if response.status_code >= 400:
      print(response.status_code, response.text)
    return response.json()

  def post(self, uri, data):
    response = requests.post(self.url + uri, data, headers=self.headers).json()
    if response.status_code >= 400:
      print(response.status_code, response.text)
    return response 

  async def async_get_all(self, loop, uri, params_list):
    async with ClientSession(loop=loop) as session:
      tasks = [asyncio.create_task(self._async_get(session, uri, params)) for params in params_list]
      return await asyncio.gather(*tasks)

  async def _async_get(self, session: ClientSession, uri, params):
    response = await session.get(self.url + uri, params=params, headers=self.headers)
    json = await response.json()
    return (params['symbol'], json)

