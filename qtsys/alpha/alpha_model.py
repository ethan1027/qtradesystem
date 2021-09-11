from abc import ABC, abstractmethod

class AlphaModel(ABC):

  @abstractmethod
  def on_bar(self, data, position, time):
    raise NotImplementedError('should implement on_bar()')
    