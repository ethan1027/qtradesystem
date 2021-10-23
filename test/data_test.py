from qtsys.data.tradier_data import TradierData
from qtsys.data.yahoo_data import YahooData

def test_yahoo_daily_bars():
  data = YahooData()
  daily_bars = data.download_bars('NVDA TSLA', start='2021-05-02', end='2021-08-01')
  print(daily_bars)
  assert daily_bars is not None
  
def test_tradier_daily_bars():
  daily_bars = TradierData('paper').download_bars('NVDA TSLA', start='2021-05-02', end='2021-08-01', interval='daily')
  print(daily_bars)
  assert daily_bars is not None

def test_yahoo_hourly_bars():
  hourly_bars = YahooData().download_bars('NVDA', start='2021-05-02', end='2021-05-05', interval='1h')
  print(hourly_bars)
  assert hourly_bars is not None

def test_tradier_hourly_bars():
  hourly_bars = TradierData('live').download_bars('NVDA TSLA', start='2021-10-22', end='2021-11-23')
  print(hourly_bars) 
  assert hourly_bars is not None

def test_yahoo_min_bars():
  pass

def test_tradier_min_bars():
  pass
