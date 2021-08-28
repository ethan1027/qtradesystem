import pyEX
from qtsys.global_config import global_config
class IEX:
  def __init__(self):
    self.client = pyEX.Client(api_token=global_config['iex']['token'])