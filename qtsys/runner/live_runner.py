from datetime import timedelta
from qtsys.data.yahoo_data import YahooData
from qtsys.data.tradier_data import TradierData
from qtsys.alpha.alpha_model import AlphaModel
from qtsys.selector.universe_selector import UniverseSelector
from qtsys.portfolio.equal_portfolio_opt import EqualPortfolioOpt
def run(
  alpha_model: AlphaModel,
  universe_selector: UniverseSelector,
  broker: Broker
  portfolio_opt=EqualPortfolioOpt(),
  interval=timedelta(hours=1),
  offset=timedelta(minutes=1),
  selection_interval=timedelta(days=1),
  data_provider=YahooData()
):