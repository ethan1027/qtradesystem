
import research.pystorew as pystorew
def test_selection():
  pystorew.write_selection('test_broker', ['AAPL', 'MSFT'])
  selection = pystorew.read_selection('test_broker')
  print(selection)
  latest_selection = pystorew.read_latest_selection('test_broker')
  print(latest_selection)
  assert latest_selection == 'AAPL MSFT'
  