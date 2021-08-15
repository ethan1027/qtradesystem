from abc import ABC, abstractmethod
from typing import List
from qtsys.broker.broker import Position


class AlphaModel(ABC):

  @abstractmethod
  def on_bar(self, data, positions: List[Position], time):
    raise NotImplementedError('should implement on_bar()')
    