from typing import Dict


class EqualPositionSizer():
  def size(self, symbols: str) -> Dict[str, float]:
    return {symbol: 100 // len(symbols) / 100 for symbol in symbols.split(' ') }