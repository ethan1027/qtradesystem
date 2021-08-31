import pyEX
from qtsys.global_config import global_config
class IEX:
  def __init__(self):
    token = global_config['iex']['token'])
    self.client = pyEX.Client(api_token=token)
    self.token = token