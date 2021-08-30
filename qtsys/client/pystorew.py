import pystore as ps

ps.set_path('C:/Users/quane/GitProjects/pystoredata')
store = ps.store('mystore')

def write(provider: str, interval: str, symbol: str, df):
  c = store.collection(provider)
  name = f'{interval}/{symbol}'
  c.append(name, df)
