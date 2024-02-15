from abc import ABC, abstractmethod

from loggers.LoggerEnum import LoggerEnum


class Logger(ABC):
    def __init__(self, device: LoggerEnum):
        self.device = device
        self.listener = None

    @abstractmethod
    def create_listener(self) -> None:
        pass

    def run(self) -> None:
        self.listener.start()

    def stop(self) -> None:
        self.listener.stop()
