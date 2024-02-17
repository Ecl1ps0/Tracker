import keyboard

from ClipboardTracker import ClipboardTracker
from configs.file_writers import save_to_report, save_clipboard_content
from configs.hotkeys import double_hotkeys
from configs.logger import get_logger
from loggers.KeyboardLogger import KeyboardLogger
from loggers.MouseLogger import MouseLogger


def main():
    logger = get_logger(__name__)

    logger.info("Start tracking actions")
    for shortcut, name in double_hotkeys:
        keyboard.add_hotkey(shortcut,
                            lambda shortcut_name: save_to_report(shortcut_name, path=".\\report.txt"),
                            args=(name,))

    clipboard_tracker = ClipboardTracker(save_clipboard_content)

    keyboard_logger = KeyboardLogger()
    keyboard_logger.create_listener()

    mouse_logger = MouseLogger()
    mouse_logger.create_listener()

    try:
        clipboard_tracker.start()
        keyboard_logger.run()
        mouse_logger.run()
        logger.info("Clipboard, mouse and keyboard tracker have started")
    except KeyboardInterrupt:
        keyboard_logger.stop()
        mouse_logger.stop()
        clipboard_tracker.stop()
        logger.info("Stop tracking")


if __name__ == '__main__':
    main()
