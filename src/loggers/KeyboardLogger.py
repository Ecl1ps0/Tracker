import ctypes
import time
from datetime import datetime

from pynput.keyboard import Listener, Key, KeyCode

from configs.file_writers import save_to_report_with_time
from configs.languages_mapping import english_to_russian_mapping, russian_to_english_mapping
from configs.logger import get_logger
from loggers.Logger import Logger

logger = get_logger(__name__)


class KeyboardLogger(Logger):
    def __init__(self):
        super(KeyboardLogger, self).__init__()

        self.start_time = time.time()
        self.start_word_time = time.time()
        self.start_row_time = time.time()

        self.initial_language = self.__get_current_language_hash()

        self.typed_characters = 0
        self.num_of_keystrokes = 0
        self.num_of_func_keys = 0

    def create_listener(self) -> Listener:
        self.listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
        return self.listener

    def __on_press(self, key: Key | KeyCode) -> None:
        self.num_of_keystrokes += 1

        if isinstance(key, Key):
            self.num_of_func_keys += 1

    def __on_release(self, key: Key | KeyCode) -> None:
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        if isinstance(key, Key):
            save_to_report_with_time(key.name + " " + datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3] + "\n")
            print(key.name)

        elif isinstance(key, KeyCode):
            current_language = self.__get_current_language_hash()

            if self.initial_language == '0x419' and current_language == '0x409':
                try:
                    save_to_report_with_time(russian_to_english_mapping[str(key.char)] + "\n")
                    logger.info(russian_to_english_mapping[str(key.char)])
                    print(russian_to_english_mapping[str(key.char)])
                except KeyError:
                    logger.info(f"Unknown KeyCode: {key}")
            elif self.initial_language == '0x409' and current_language == '0x419':
                try:
                    save_to_report_with_time(english_to_russian_mapping[str(key.char)] + "\n")
                    print(english_to_russian_mapping[str(key.char)])
                except KeyError:
                    logger.info(f"Unknown KeyCode: {key}")
            else:
                save_to_report_with_time(str(key.char) + " " + datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3] + "\n")
                logger.info(str(key.char))
                print(str(key.char))

            self.typed_characters += 1

            if elapsed_time > 0:
                cpm = (self.typed_characters / elapsed_time) * 60
                save_to_report_with_time(f"CPM={cpm:.2f}\n")
                logger.info(f"CPM={cpm:.2f}")
                print(f"CPM={cpm:.2f}")

    @staticmethod
    def __get_current_language_hash() -> str:
        user32 = ctypes.WinDLL('user32.dll', use_last_error=True)
        current_window = user32.GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(current_window, 0)
        klid = user32.GetKeyboardLayout(thread_id)
        lid = klid & (2 ** 16 - 1)
        return hex(lid)
