from abc import abstractmethod, ABC

class BaseWidget(ABC):
    def __init__ (self, config):
        self.config = config

    @abstractmethod
    def update_all(self, now):
        raise NotImplementedError

    @abstractmethod
    def render(self, window):
        raise NotImplementedError