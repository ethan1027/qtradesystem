from qtsys.client.tradier import TradierClient


def test_tradier_client():
  client = TradierClient()
  assert client.account_id is not None
  