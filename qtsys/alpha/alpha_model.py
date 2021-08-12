from abc import ABC, abstractmethod

class AlphaModel(ABC):
  def __init__(self):
    pass

  @abstractmethod
  def on_bar(self, data):
    raise NotImplementedError('should implement on_bar()')
    
  def run(self, data):
    self.on_bar(data)