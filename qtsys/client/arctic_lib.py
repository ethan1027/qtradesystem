from arctic import Arctic

a = Arctic('mongodb://localhost:27017')
a.initialize_library('vstore')
lib = a['vstore']

def write(provider: str, interval: str, symbol: str,  df):
  name = f'{provider}_{interval}_{symbol}'
  lib.append(name, df)

def read(provider: str, interval: str, symbol: str):
  name = f'{provider}_{interval}_{symbol}'
  return lib.read(name)

  