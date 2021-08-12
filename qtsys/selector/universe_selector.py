from abc import ABC, abstractmethod


class UniverseSelector(ABC):
  
  @abstractmethod
  def on_selection(self, cur_date, data):
    pass

  def run(self, cur_date, data):
    self.on_selection(cur_date, data)