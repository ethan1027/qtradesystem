from qtsys.data.tradier_data import TradierData
from qtsys.data.yahoo_data import YahooData

def test_tradier_download_bars():
  daily_bars = TradierData().download_bars('NVDA', start='2021-05-02', end='2021-08-01')
  print(daily_bars.loc['2021-04-03':'2021-05-20'])



def test_yahoo_download_bars():
  daily_bars = YahooData().download_bars('NVDA', start='2021-05-02', end='2021-08-01')
  print(daily_bars.loc['2021-04-03':'2021-05-20'])
  hourly_bars = YahooData().download_bars('NVDA', start='2021-05-02', end='2021-05-05', interval='1h')
  print(hourly_bars)