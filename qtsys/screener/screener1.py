from typing import List
from qtsys.data.data_bundle import DataBundle
from qtsys.screener.asset_screener import AssetScreener


class Screener1(AssetScreener):
  def screen(self, data: DataBundle) -> List[str]:
    return ['HIMX', 'DE', 'KLIC', 'VRT', 'NTNX']
