import pytest
from qtsys import backtest_runner, live_runner

@pytest.mark.skip()
def test_backtest_runner():
  live_runner.run(None, None, None)