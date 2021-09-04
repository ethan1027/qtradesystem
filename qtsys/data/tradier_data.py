import asyncio
import pandas as pd

from qtsys.data.util import resample_bar_data
from qtsys.client.tradier import TradierClient
from qtsys.data.market_data import MarketData
from qtsys.client import pystorew


class TradierData(MarketData):

  _resample_interval = {
    '2min': '1min',
    '30min': '15min',
    '60min': '15min',
  }

  def __init__(self):
    self.client = TradierClient(trading_mode=False, account_type='live')

  def download_bars(self, symbols: str, start=None, end=None, interval='60min'):
    interval = self._resample_interval[interval] if interval in self._resample_interval else interval
    params_list = [self._create_data_params(symbol, start, end, interval) for symbol in symbols.split(' ')]
    loop = asyncio.get_event_loop()
    if interval == 'daily':
      results = loop.run_until_complete(self.client.async_get_all(loop, '/v1/markets/history', params_list))
      bars_dict = dict(results)
      for symbol, bars in bars_dict.items():
        df = pd.json_normalize(bars['history']['day'])
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
        bars_dict[symbol] = df
      return bars_dict
    else:
      results = loop.run_until_complete(self.client.async_get_all(loop, '/v1/markets/timesales', params_list))
      bars_dict = dict(results)
      for symbol, bars in bars_dict.items():
        df = pd.json_normalize(bars['series']['data'])
        df.set_index('time', inplace=True)
        df.index = pd.to_datetime(df.index)
        if interval in self._resample_interval:
          df = resample_bar_data(df, interval)
        bars_dict[symbol] = df
      return bars_dict

  def save_bars(self, symbols: str, start=None, end=None, interval='60min'):
    bars_dict = self.download_bars(symbols, start, end, interval)
    for symbol, df in bars_dict.items():
      pystorew.write_bars('tradier', interval, symbol, df)


  
  def get_historical_bars(self, symbol, current_date):
    # return self._historical_bars[symbol][:current_date][:-1]
    pass

  def _create_data_params(self, symbol, start, end, interval):
    return {'symbol': symbol, 'interval': interval, 'start': start, 'end': end}
