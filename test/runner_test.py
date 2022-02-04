from datetime import timedelta
import pytest
from qtsys import live_trade

@pytest.mark.skip()
def test_backtest_runner():
  live_trade.run(None, None, None, interval=timedelta(minutes=3))

def test_start_time():
  print(live_trade.get_start_datetime())
