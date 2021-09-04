from qtsys.data.data_bundle import DataBundle
from qtsys.selector.universe_selector import UniverseSelector
import pyEX


class SampleSelector(UniverseSelector):
  def select(self, data: DataBundle):
    token = data.iex.token
    # c = pyEX.collectionsDF(tag='list', collectionName='mostactive', token=token)
    # print(c)
    pyEX.largestTrades('TSLA', token=token)

    