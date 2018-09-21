from abc import abstractmethod
from abc import ABC


class BaseBehavior(ABC):
    def __init__(self, params={}):
        self.params = params

    @abstractmethod
    def execute(self):
        pass
