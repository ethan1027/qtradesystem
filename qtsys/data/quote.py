class Quote:
  def __init__(self,
    symbol: str,
    asset_type: str,
    last: float,
    change: float,
    volume: int,
    open_price: float,
    close_price: float,
    high: float,
    low: float,
    bid: float,
    bid_size: int,
    ask: float,
    ask_size: int,
    week_52_high: float,
    week_52_low: float
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
    return Quote(
      quote.get('symbol'),
      quote.get('type'),
      quote.get('last'),
      quote.get('change'),
      quote.get('volume'),
      quote.get('open'),
      quote.get('open'),
      quote.get('close'),
      quote.get('low'),
      quote.get('bid'),
      quote.get('bidsize'),
      quote.get('ask'),
      quote.get('asksize'),
      quote.get('week_52_high'),
      quote.get('week_52_low')
    )
