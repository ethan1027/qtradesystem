import asyncio
from qtsys.data.util import resample_bar_data

from qtsys.client.tradier import TradierClient
import pandas as pd
from qtsys.data.market_data import MarketData


class TradierData(MarketData):
  interval_param = {
    '1d': 'daily',
    '1m': '1min',
    '5m': '5min',
    '15m': '15min',
    '30m': '15min',
    '1h': '15min'
  }

  resample_param = {
    '30m': '30min',
    '1h': '60min'
  }

  def __init__(self):
    self.client = TradierClient(trading_mode=False, account_type='live')

  def download_bars(self, symbols: str, start=None, end=None, interval='1d'):
    params_list = [self._create_data_params(symbol, start, end, interval) for symbol in symbols.split(' ')]
    loop = asyncio.get_event_loop()
    if interval[-1] == 'd':
      results = loop.run_until_complete(self.client.async_get_all(loop, '/v1/markets/history', params_list))
      bars_dict = dict(results)
      for symbol, bars in bars_dict.items():
        df = pd.json_normalize(bars['history']['day'])
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index) # type: ignore
        bars_dict[symbol] = df
      return bars_dict
    else:
      results = loop.run_until_complete(self.client.async_get_all(loop, '/v1/markets/timesales', params_list))
      bars_dict = dict(results)
      for symbol, bars in bars_dict.items():
        df = pd.json_normalize(bars['series']['data'])
        df.set_index('time', inplace=True)
        df.index = pd.to_datetime(df.index) # type: ignore
        if interval in self.resample_param.keys():
          resample_bar_data(df, self.resample_param[interval])
        bars_dict[symbol] = df
      return bars_dict
   
  def save_bars(self, symbols: str, start=None, end=None, interval='1d'):
    self._historical_bars = self.download_bars(symbols, start, end, interval)
  
  def get_historical_bars(self, symbol, current_date):
    return self._historical_bars[symbol][:current_date][:-1]

  def _create_data_params(self, symbol, start, end, interval):
    return {'symbol': symbol, 'interval': self.interval_param[interval], 'start': start, 'end': end}

