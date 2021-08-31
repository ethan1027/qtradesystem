from abc import ABC, abstractmethod
from qtsys.data.data_bundle import DataBundle
from typing import List


class UniverseSelector(ABC):
  
  @abstractmethod
  def select(self, data: DataBundle) -> List[str]:
    pass

