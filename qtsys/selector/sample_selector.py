from qtsys.data.data_bundle import DataBundle
from qtsys.selector.universe_selector import UniverseSelector
from finviz import Screener


class SampleSelector(UniverseSelector):
  def select(self, data: DataBundle):
    filters = ['fa_epsyoy_pos', 'geo_usa', 'sh_avgvol_o1000', 'sh_curvol_o2000', 'ta_changeopen_u1' , 'ta_sma200_pa']
    screener = Screener(filters=filters, order='-volume')
    symbols = screener['Ticker']
    