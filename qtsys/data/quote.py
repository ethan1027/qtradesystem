class Quote:
  def __init__(self, 
    symbol,
    asset_type,
    last,
    change,
    volume,
    open_price,
    close_price,
    high,
    low,
    bid,
    bid_size,
    ask,
    ask_size,
    week_52_high,
    week_52_low
  ):
    self.symbol = symbol
    self.asset_type = asset_type
    self.last = last
    self.change = change
    self.volume = volume
    self.open_price = open_price
    self.close_price = close_price
    self.high = high
    self.low = low
    self.bid = bid
    self.bid_size = bid_size
    self.ask = ask
    self.ask_size = ask_size
    self.week_52_high = week_52_high
    self.week_52_low = week_52_low

  @staticmethod
  def from_tradier_quote(quote):
    symbol: str = quote.get('symbol')
    asset_type: str = quote.get('type')
    last: float = quote.get('last')
    change: float = quote.get('change')
    volume: int = quote.get('volume')
    open_price: float = quote.get('open')
    close_price: float = quote.get('close')
    high: float = quote.get('high')
    low: float = quote.get('low')
    bid: float = quote.get('bid')
    bid_size: int = quote.get('bidsize')
    ask: float = quote.get('ask')
    ask_size: int = quote.get('asksize')
    week_52_high: float = quote.get('week_52_high')
    week_52_low: float = quote.get('week_52_low')
    return Quote(symbol, asset_type, last, change, volume,
      open_price, close_price, high, low, bid, bid_size, ask, ask_size,
      week_52_high, week_52_low)

