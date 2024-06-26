import logging

from pynput import keyboard, mouse

from ClipboardTracker import ClipboardTracker


class LoggerHandler:
    def __init__(self, trackers: list[ClipboardTracker | keyboard.Listener | mouse.Listener], logger: logging.Logger):
        self.trackers = trackers
        self.logger = logger

    def start_tracking(self) -> None:
        for tracker in self.trackers:
            if not tracker.is_alive():
                self.logger.info(f"Start {type(tracker).__name__}")
                tracker.start()

    def stop_tracking(self) -> None:
        for tracker in self.trackers:
            self.logger.info(f"Stop {type(tracker).__name__}")
            tracker.stop()
