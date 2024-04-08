import ctypes
import time

from pynput.keyboard import Listener, Key, KeyCode

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
        self.typed_words = 0
        self.typed_sentences = 0
        self.typed_rows = 0

    def create_listener(self) -> Listener:
        self.listener = Listener(on_press=self.__on_press, on_release=self.__on_realese)
        return self.listener

    def __on_press(self, key: Key | KeyCode) -> None:
        pass

    def __on_realese(self, key: Key | KeyCode) -> None:
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        with open(".\\report.txt", "a") as file:
            if isinstance(key, Key):
                file.write(key.name + "\n")
                print(key.name)

                if key.name == "space":
                    self.typed_words += 1
                    wpm = (self.typed_words / elapsed_time) * 60
                    file.write(f"WPM={wpm:.2f}\n")
                    logger.info(f"WPM={wpm:.2f}")
                    print(f"WPM={wpm:.2f}")

                    end_word_time = time.time()
                    word_typing_pause = end_word_time - self.start_word_time
                    file.write(f"Pause between words = {word_typing_pause:.2f}\n")
                    logger.info(f"Pause between words = {word_typing_pause:.2f}")
                    print(f"Pause between words = {word_typing_pause:.2f}")
                    self.start_word_time = time.time()

                if key.name == "enter":
                    self.typed_rows += 1
                    rpm = (self.typed_rows / elapsed_time) * 60
                    file.write(f"RPM={rpm:.2f}\n")
                    logger.info(f"RPM={rpm:.2f}")
                    print(f"RPM={rpm:.2f}")

                    end_row_time = time.time()
                    row_typing_pause = end_row_time - self.start_row_time
                    file.write(f"Pause between rows = {row_typing_pause:.2f}\n")
                    logger.info(f"Pause between rows = {row_typing_pause:.2f}")
                    print(f"Pause between rows = {row_typing_pause:.2f}")
                    self.start_row_time = time.time()

            elif isinstance(key, KeyCode):
                current_language = self.__get_current_language_hash()

                if self.initial_language == '0x419' and current_language == '0x409':
                    try:
                        file.write(russian_to_english_mapping[str(key.char)] + "\n")
                        logger.info(russian_to_english_mapping[str(key.char)])
                        print(russian_to_english_mapping[str(key.char)])
                    except KeyError:
                        logger.info(f"Unknown KeyCode: {key}")
                elif self.initial_language == '0x409' and current_language == '0x419':
                    try:
                        file.write(english_to_russian_mapping[str(key.char)] + "\n")
                        print(english_to_russian_mapping[str(key.char)])
                    except KeyError:
                        logger.info(f"Unknown KeyCode: {key}")
                else:
                    file.write(str(key.char) + "\n")
                    logger.info(str(key.char))
                    print(str(key.char))

                self.typed_characters += 1

                if key.char in ['.', '!', '?']:
                    self.typed_sentences += 1
                    spm = (self.typed_sentences / elapsed_time) * 60
                    file.write(f"SPM={spm:.2f}\n")
                    logger.info(f"SPM={spm:.2f}")
                    print(f"SPM={spm:.2f}")

                if elapsed_time > 0:
                    cpm = (self.typed_characters / elapsed_time) * 60
                    file.write(f"CPM={cpm:.2f}\n")
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
