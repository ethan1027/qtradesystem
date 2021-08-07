from dotenv import dotenv_values
import requests

TRADIER_TOKEN = dotenv_values('.env')['TRADIER_TOKEN']
TRADIER_SANDBOX_TOKEN = dotenv_values('.env')['TRADIER_SANDBOX_TOKEN']

TRADIER_URL = 'https://api.tradier.com'
TRADIER_SANDBOX_URL = 'https://sandbox.tradier.com'

class TradierClient():
  def __init__(self, env: str):
    self.env = env
    if env == 'live':
      self.url = TRADIER_URL
      self.token = TRADIER_TOKEN
    else:
      self.url = TRADIER_SANDBOX_URL
      self.token = TRADIER_SANDBOX_TOKEN

  def http_get(self, uri, params):
    return requests.get(self.url + uri, params=params, headers={'Authorization': f'Bearer {self.token}', 'Accept': 'application/json'}).json()