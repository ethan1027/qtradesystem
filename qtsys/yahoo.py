import yfinance as yf
import pandas as pd
from qtsys.data import MarketData

class YahooData(MarketData):
  def get_bars(self, symbols: str, start, end=None, interval='1d'):
    data: pd.DataFrame = yf.download(symbols, start=start, end=end, interval=interval)
    # rename column from left to right
    columns = {
      'Adj Close': 'adj_close',
      'Low': 'low', 
      'High': 'high', 
      'Open': 'open', 
      'Close': 'close', 
      'Volume': 'volume'
    }
    data.rename(columns=columns, inplace=True)
    data = data.rename_axis(index={'Date':'date'}) 
    return data

  def get_quotes(self, symbols: str):
    pass
  