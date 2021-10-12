from abc import abstractmethod
from typing import Dict, List


class PositionSizer:
  @abstractmethod
  def size(self, symbols) -> Dict[str, float]:
    pass

  def run_sizing(self, symbols: List[str]) -> Dict[str, float]:
    desired_positions = self.size(symbols)
    if sum(desired_positions.values()) > 1:
      raise RuntimeError('position sizes must add up to 1 or less')
    return desired_positions

