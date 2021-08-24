from qtsys.client.tradier import TradierClient
import pandas as pd
from qtsys.data.market_data import MarketData


class TradierData(MarketData):
  interval_ref = {
    '1d': 'daily',
    '1m': '1min',
    '15m': '15min',
    '30m': '15min',
    '1h': '15min'
  }

  resample_factor = {
    '30m': 2,
    '1h': 4
  }

  def __init__(self):
    self.client = TradierClient()

  def download_bars(self, symbols, start=None, end=None, interval='1d'):
    params = {'symbol': symbols, 'interval': self.interval_ref[interval], 'start': start, 'end': end}
    json = self.client.get('/v1/markets/history', params)
    df = pd.json_normalize(json['history']['day'])
    df.set_index('date', inplace=True)
    self._historical_bars = df
  
  def get_historical_bars(self, symbol, current_date):
    return self._historical_bars[:current_date][:-1]

