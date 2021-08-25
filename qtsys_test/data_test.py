from qtsys.data.tradier_data import TradierData
from qtsys.data.yahoo_data import YahooData

def test_yahoo_daily_bars():
  data = YahooData()
  daily_bars = data.download_bars('NVDA TSLA', start='2021-05-02', end='2021-08-01')
  print(daily_bars)
  assert daily_bars is not None
  
def test_tradier_daily_bars():
  daily_bars = TradierData().download_bars('NVDA TSLA', start='2021-05-02', end='2021-08-01')
  print(daily_bars)
  assert daily_bars is not None

def test_yahoo_hourly_bars():
  hourly_bars = YahooData().download_bars('NVDA', start='2021-05-02', end='2021-05-05', interval='1h')
  print(hourly_bars)
  assert hourly_bars is not None

def test_tradier_hourly_bars():
  hourly_bars = TradierData().download_bars('NVDA TSLA', start='2021-08-24 09:30', end='2021-08-24 16:00', interval='1h')
  print(hourly_bars) 
  assert hourly_bars is not None

def test_yahoo_min_bars():
  pass

def test_tradier_min_bars():
  pass
