from qtsys.data.tradier_data import TradierData
from qtsys.data.yahoo_data import YahooData

def test_tradier_download_bars():
  bars = TradierData().download_bars('NVDA', start='2021-05-02', end='2021-08-01')
  print(bars)
  print(bars.loc[:'2021-06-02'])


def test_yahoo_download_bars():
  bars = YahooData().download_bars('NVDA', start='2021-05-02', end='2021-08-01')
  print(bars)