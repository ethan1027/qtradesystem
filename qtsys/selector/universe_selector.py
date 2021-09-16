from abc import ABC, abstractmethod
from typing import List
from qtsys.data.data_bundle import DataBundle

class UniverseSelector(ABC):

  @abstractmethod
  def select(self, data: DataBundle) -> List[str]:
    pass
