from typing import List
import yfinance as yf
from qtsys.data.market_data import MarketData

class YahooData(MarketData):
  def download_bars(self, symbols: str, start, end=None, interval='1d'):
    df = yf.download(symbols, start=start, end=end, interval=interval)
    df.rename(columns={'Adj Close': 'adj_close', 'Low': 'low', 'High': 'high', 'Open': 'open', 'Close': 'close', 'Volume': 'volume'}, inplace=True) 
    df = df.rename_axis(index={'Date':'date'})
    return df