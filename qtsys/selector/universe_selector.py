from abc import ABC, abstractmethod
from typing import List
from qtsys.data.data_bundle import DataBundle
from qtsys.client import pystorew

class UniverseSelector(ABC):

  @abstractmethod
  def select(self, data: DataBundle) -> List[str]:
    pass

  def run_selection(self, data: DataBundle, broker_id: str):
    symbols = self.select(data)
    df = pd.DataFrame()
    pystorew.write_selection()

