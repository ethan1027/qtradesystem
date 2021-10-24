from typing import Dict, List

from qtsys.sizer.position_sizer import PositionSizer


class EqualPositionSizer(PositionSizer):
  def size(self, symbols: List[str]) -> Dict[str, float]:
    return {symbol: 100 // len(symbols) / 100 for symbol in symbols }