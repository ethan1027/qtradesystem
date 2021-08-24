import asyncio
from re import split
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
    self.client = TradierClient(trading_mode=False, account_type='live')

  def download_bars(self, symbols: str, start=None, end=None, interval='1d'):
    params_list = [self._create_data_params(symbol, start, end, interval) for symbol in symbols.split(' ')]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(self.client.async_get_all(loop, '/v1/markets/history', params_list))
    bars_dict = dict(results)
    for symbol, bars in bars_dict: 
      df = pd.json_normalize(bars['history']['day'])
      df.set_index('date', inplace=True)
      bars_dict[symbol] = df
    return bars_dict

  def save_bars(self, symbols: str, start=None, end=None, interval='1d'):
    self._historical_bars = self.download_bars(symbols, start, end, interval)
  
  def get_historical_bars(self, symbol, current_date):
    return self._historical_bars[symbol][:current_date][:-1]

  def _create_data_params(self, symbol, start, end, interval):
    return {'symbol': symbol, 'interval': self.interval_ref[interval], 'start': start, 'end': end}

