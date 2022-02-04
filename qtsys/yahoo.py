import yfinance as yf
import pandas as pd
from qtsys.data import MarketData

class YahooData(MarketData):
  def get_historical_bars(self, symbols: str, start, end=None, interval='1d'):
    df = yf.download(symbols, start=start, end=end, interval=interval) # type: pd.DataFrame
    columns = {
      'Adj Close': 'adj_close',
      'Low': 'low', 
      'High': 'high', 
      'Open': 'open', 
      'Close': 'close', 
      'Volume': 'volume'
    }
    df.rename(columns=columns, inplace=True)
    df = df.rename_axis(index={'Date':'date'}) 
    return df

  def get_quotes(self, symbol: str):
    pass
  