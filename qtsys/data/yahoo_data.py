import yfinance as yf
from qtsys.data.market_data import MarketData

class YahooData(MarketData):
  def download_bars(symbols, period, start, end, interval):
    parsed_symbols = ' '.join(symbols)
    data = yf.download(parsed_symbols, period=period, start=start, end=end)
    return data