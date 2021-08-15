import yfinance as yf
import pandas as pd
from qtsys.data.market_data import MarketData

class YahooData(MarketData):
  def download_bars(self, symbols: str, start, end=None, interval='1d'):
    df = yf.download(symbols, start=start, end=end, interval=interval)
    columns = {
      'Adj Close': 'adj_close',
      'Low': 'low', 
      'High': 'high', 
      'Open': 'open', 
      'Close': 'close', 
      'Volume': 'volume'
    }
    df.rename(columns=columns, inplace=True) # type: ignore 
    df = df.rename_axis(index={'Date':'date'}) # type: ignore
    self.historical_bars = df

  def get_historical_bars(self, symbol, current_date):
    self.historical_bars.query('')
  

  @property
  def historical_bars(self) -> pd.DataFrame:
    return self._historical_bars
    
  @historical_bars.setter
  def historical_bars(self, value: pd.DataFrame):
    self._historical_bars = value

  