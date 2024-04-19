from abc import ABC, abstractmethod


class Logger(ABC):
    def __init__(self):
        self.listener = None

    @abstractmethod
    def create_listener(self) -> None:
        pass
