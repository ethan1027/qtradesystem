import yfinance as yf
from tradesys.data.feed import Feed

class YahooFeed(Feed):
  def get_bars(symbols, period, start, end, interval):
    parsed_symbols = ' '.join(symbols)
    data = yf.download(parsed_symbols, period=period, start=start, end=end)
    return data