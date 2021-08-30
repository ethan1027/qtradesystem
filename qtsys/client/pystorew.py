import pystore as ps

ps.set_path('C:/Users/quane/GitProjects/pystoredata')
store = ps.store('mystore')
c = store.collection('tradier')

def write(provider: str, interval: str, symbol: str,  df):
  name = f'{interval}/{symbol}'
  c.append(name, df)
