from qtsys.data.tradier_data import TradierData

def test_download_bars():
  bars = TradierData().download_bars('NVDA', start='2021-05-02', end='2021-07-10')
  print(bars)