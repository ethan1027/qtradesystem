import asyncio
from aiohttp import ClientSession
import requests
from qtsys.global_config import global_config



class TradierClient:
  def __init__(self, trading_mode: bool = False, account_type: str = 'paper'):
    self.url = global_config['tradier'][account_type]['url']
    self.token = global_config['tradier'][account_type]['token']
    self.headers = {'Authorization': f'Bearer {self.token}', 'Accept': 'application/json'}
    print('using endpoint', self.url)
    if trading_mode:
      print('getting account profile...')
      profile = self.get('/v1/user/profile')
      print('using profile:', profile)
      self.account_id = profile['profile']['account']['account_number']

  def get(self, uri, params=None):
    response = requests.get(self.url + uri, params=params, headers=self.headers)
    print(response.status_code)
    print(response.text)
    return response.json()

  def post(self, uri, data):
    return requests.post(self.url + uri, data, headers=self.headers).json()

  async def async_get_all(self, loop, uri, params_list):
    async with ClientSession(loop=loop) as session:
      tasks = [asyncio.create_task(self._async_get(session, uri, params)) for params in params_list]
      return await asyncio.gather(*tasks)

  async def _async_get(self, session: ClientSession, uri, params):
    response = await session.get(self.url + uri, params=params, headers=self.headers)
    json = await response.json()
    return (params['symbol'], json)
