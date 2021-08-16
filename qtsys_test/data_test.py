from qtsys.client.tradier import TradierClient
from qtsys.data.tradier_data import TradierData
from qtsys.data.yahoo_data import YahooData
def test_yahoo_download_bars():
  data = YahooData()
  data.download_bars('NVDA TSLA MSFT AMD', start='2021-05-02', end='2021-08-01')
  bars = data.get_historical_bars('NVDA', '2021-06-02')
  print(bars)
  assert bars is not None
  YahooData().download_bars('NVDA', start='2021-05-02', end='2021-05-05', interval='1h')
  hourly_bars = data.get_historical_bars('NVDA', '2021-06-02')

def test_tradier_download_bars():
  data = TradierData(TradierClient())
  data.download_bars('NVDA', start='2021-05-02', end='2021-08-01')
  bars = data.get_historical_bars('NVDA', '2021-06-02')
  print(bars)
  assert bars is not None
