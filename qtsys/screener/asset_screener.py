from abc import ABC, abstractmethod
from typing import List
from qtsys.data.data_bundle import DataBundle
from qtsys.client import pystorew

class AssetScreener(ABC):

  @abstractmethod
  def screen(self, data: DataBundle) -> List[str]:
    pass

  def run_screen(self, data: DataBundle, broker_id: str):
    symbols = self.screen(data)
    pystorew.write_selection(broker_id, symbols)

