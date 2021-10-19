from qtsys.client.tradier import TradierClient


def test_tradier_client():
  client = TradierClient(trading_mode=True)
  assert client.account_id is not None
  