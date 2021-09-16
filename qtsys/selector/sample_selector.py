from finviz import Screener
from qtsys.data.data_bundle import DataBundle
from qtsys.selector.universe_selector import UniverseSelector


class SampleSelector(UniverseSelector):
  def select(self, data: DataBundle):
    filters = ['fa_epsyoy_pos', 'geo_usa', 'sh_avgvol_o1000', 'sh_curvol_o2000', 'ta_changeopen_u1' , 'ta_sma200_pa']
    results = Screener(filters=filters, order='-volume')
    symbols = [result['Ticker'] for result in results]
    quotes = data.tradier.get_quotes(' '.join(symbols))
    symbols = [symbol for symbol in symbols if 10 <= quotes[symbol]['last'] <= 200]
    return symbols
    