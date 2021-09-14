from typing import List


class EqualPortfolioOpt():
  def optimize(self, symbols: List[str]):
    return {symbol: 100 // len(symbols) / 100 for symbol in symbols }