import pystore as ps

ps.set_path('C:/Users/quane/GitProjects/pystoredata')
store = ps.store('mystore')

def write_bars(provider, interval, symbol, df):
  c = store.collection(f'{provider}.{interval}')
  c.append(symbol, df)

def read_bars(provider, interval, symbol):
  c = store.collection(f'{provider}.{interval}')
  return c.item(symbol)

def write_selection(broker_id: str, df):
  c = store.collection(f'{broker_id}')
  c.append('selection', df)

def write_order(broker_id, df):
  pass

def write_positions(broker_id, df):
  pass
