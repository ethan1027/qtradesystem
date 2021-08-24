from dotenv import dotenv_values
import asyncio
from aiohttp import ClientSession
import requests

TRADIER_TOKEN = dotenv_values('.env')['TRADIER_TOKEN']

TRADIER_URL = 'https://api.tradier.com'

HEADERS = {'Authorization': f'Bearer {TRADIER_TOKEN}', 'Accept': 'application/json'}

class TradierClient:
  def __init__(self, trading_mode = False):
    if trading_mode:
      print('getting account profile...')
      profile = self.get('/v1/user/profile')
      print(profile)
      self._account_id = profile['profile']['account']

  def get(self, uri, params=None):
    return requests.get(TRADIER_URL + uri, params=params, headers=HEADERS).json()

  def post(self, uri, data):
    return requests.get(TRADIER_URL + uri, data)

  async def async_get(self, loop, uri, params_list):
    async with ClientSession(loop=loop) as session:
      return await asyncio.gather(*[self._async_task_get(session, uri, params) for params in params_list])
  
  async def _async_task_get(self, session: ClientSession, uri, params):
    response = await session.get(TRADIER_URL + uri, params=params)
    return await response.json()

  @property
  def account_id(self):
    if not self._account_id:
      raise RuntimeError('Unable to retrieve account_id')
    return self._account_id

  @account_id.setter
  def account_id(self, v):
    self._account_id = v

    