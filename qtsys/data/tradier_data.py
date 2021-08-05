from dotenv import dotenv_values
import requests
import pandas as pd
from qtsys.data.market_data import MarketData

TRADIER_TOKEN = dotenv_values('.env')['TRADIER_TOKEN']
TRADIER_URL = 'https://api.tradier.com'

class TradierData(MarketData):
  
  interval_dict = {
    '1d': 'daily'
  }

  def download_bars(self, symbols, period=None, start=None, end=None, interval='1d'):
    params = {'symbol': symbols, 'interval': self.interval_dict[interval], 'start': start, 'end': end}
    json = self._http_get('/v1/markets/history', params)
    print(json['history'])
    return pd.json_normalize(json['history']['day'])

  def _http_get(self, uri, params):
    return requests.get(TRADIER_URL + uri, params=params, headers={'Authorization': f'Bearer {TRADIER_TOKEN}', 'Accept': 'application/json'}).json()

