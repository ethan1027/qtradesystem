from datetime import timedelta
import pytest
from qtsys import backtest_runner, live_runner

@pytest.mark.skip()
def test_backtest_runner():
  live_runner.run(None, None, None, interval=timedelta(minutes=3))

def test_start_time():
  print(live_runner._get_start_datetime())
