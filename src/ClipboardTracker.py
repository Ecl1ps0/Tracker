import threading
import time
from typing import Callable

import pyperclip


class ClipboardTracker(threading.Thread):
    def __init__(self, callback: Callable[..., None] = None, pause: float = 5.):
        super(ClipboardTracker, self).__init__()
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self) -> None:
        recent_value = ""
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value

                self._callback(recent_value)

            time.sleep(self._pause)

    def stop(self) -> None:
        self._stopping = True
