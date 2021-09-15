from abc import abstractmethod
from typing import Dict


class PortfolioOpt:
  @abstractmethod
  def optimize(self, symbols) -> Dict[str, float]:
    pass