import logging
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
  symbols_str = ' '.join(symbols)
  logging.info('saving to pystore collection: %s', symbols_str)
  df = pd.DataFrame(data={'selection': [symbols_str]}, index=[pd.Timestamp.today(tz='US/Eastern')])
  _write_or_append(c, 'selection', df)

def read_selection(broker_id):
  col = store.collection(broker_id)
  logging.info('retrieving asset selection')
  df = col.item('selection').to_pandas()
  logging.info('successfully retrieved asset selection')
  logging.info(df)
  return df

def write_order(broker_id, df):
  pass

def write_positions(broker_id, df):
  pass

def write_balances(broker_id, df):
  pass

def _write_or_append(collection, item, df):
  if item in collection.list_items():
    logging.info('item %s.%s exists, appending to it', collection, item)
    collection.append(item, df)
  else:
    logging.info('item %s.%s does not exist, create a new one', collection, item)
    collection.write(item, df)
