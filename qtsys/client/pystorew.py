from datetime import date
import symbol
import pandas as pd
from typing import List
import pystore as ps

ps.set_path('C:/Users/quane/GitProjects/pystoredata')
store = ps.store('mystore')

def write_bars(provider, interval, symbol, df):
  c = store.collection(f'{provider}.{interval}')
  _write_or_append(c, symbol, df)


def read_bars(provider, interval, symbol):
  c = store.collection(f'{provider}.{interval}')
  return c.item(symbol).data

def write_selection(broker_id, symbols: List[str]):
  c = store.collection(broker_id)
  dt = date.today() 
  symbols_str = ' '.join(symbols)
  df = pd.DataFrame(data={'selection': [symbols_str]}, index=[pd.Timestamp()])
  _write_or_append(c, 'selection', df)

def read_selection(broker_id, dt):
  c = store.collection(broker_id)
  return c.item('selection').to_pandas().iloc[dt]

def write_order(broker_id, df):
  pass

def write_positions(broker_id, df):
  pass

def write_balances(broker_id, df):
  pass

def _write_or_append(collection, item, df):
  if item not in collection.list_items():
    collection.write(item, df)
  else:
    collection.append(item, df)
