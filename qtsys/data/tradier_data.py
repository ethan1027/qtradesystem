import pandas as pd
import qtsys.client.tradier as tradier
from qtsys.data.market_data import MarketData


class TradierData(MarketData):
  interval_dict = {
    '1d': 'daily'
  }

  def download_bars(self, symbols, start=None, end=None, interval='1d'):
    params = {'symbol': symbols, 'interval': self.interval_dict[interval], 'start': start, 'end': end}
    json = tradier.http_get('/v1/markets/history', params)
    df = pd.json_normalize(json['history']['day'])
    df.set_index('date', inplace=True)
    return df
