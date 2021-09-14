from abc import abstractmethod


class PortfolioOpt:
  @abstractmethod
  def optimize(self, symbols):
    pass