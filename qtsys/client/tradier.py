from dotenv import dotenv_values
import requests

TRADIER_TOKEN = dotenv_values('.env')['TRADIER_TOKEN']

TRADIER_URL = 'https://api.tradier.com'

HEADERS = {'Authorization': f'Bearer {TRADIER_TOKEN}', 'Accept': 'application/json'}

class TradierClient:
  def __init__(self):
    print('getting account profile...')
    profile = self.http_get('/v1/user/profile')
    print(profile)
    self.account_id = profile['profile']['account']

  def http_get(self, uri, params=None):
    return requests.get(TRADIER_URL + uri, params=params, headers=HEADERS).json()

  def http_post(self, uri, data):
    return requests.get(TRADIER_URL + uri, data)