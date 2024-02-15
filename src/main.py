import keyboard

from ClipboardTracker import ClipboardTracker
from configs.file_writers import save_to_report, save_clipboard_content
from configs.hotkeys import double_hotkeys
from loggers.KeyboardLogger import KeyboardLogger
from loggers.MouseLogger import MouseLogger


def main():
    for shortcut, name in double_hotkeys:
        keyboard.add_hotkey(shortcut, lambda shortcut_name: save_to_report(shortcut_name), args=(name,))

    clipboard_tracker = ClipboardTracker(save_clipboard_content)

    keyboard_logger = KeyboardLogger()
    keyboard_logger.create_listener()

    mouse_logger = MouseLogger()
    mouse_logger.create_listener()

    try:
        clipboard_tracker.start()
        keyboard_logger.run()
        mouse_logger.run()
    except KeyboardInterrupt:
        keyboard_logger.stop()
        mouse_logger.stop()
        clipboard_tracker.stop()


if __name__ == '__main__':
    main()
