from abc import ABC, abstractmethod
from typing import List


class UniverseSelector(ABC):
  
  @abstractmethod
  def on_selection(self, cur_date) -> List[str]:
    pass

