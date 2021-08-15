from dotenv import dotenv_values
import requests

TRADIER_TOKEN = dotenv_values('.env')['TRADIER_TOKEN']

TRADIER_URL = 'https://api.tradier.com'

def http_get(uri, params):
  return requests.get(TRADIER_URL + uri, params=params, headers={'Authorization': f'Bearer {TRADIER_TOKEN}', 'Accept': 'application/json'}).json()