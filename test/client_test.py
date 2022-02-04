from qtsys.client.tradier import TradierClient
import qtsys.client.orats as orats


def test_tradier_client():
  client = TradierClient(trading_mode=True)
  assert client.account_id is not None

def test_orats_client():
  res = orats.get_data('TSLA')
  print(res.headers)
  