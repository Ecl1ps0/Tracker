import keyboard
import pynput
import ctypes

from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button

from ClipboardTracker import ClipboardTracker
from configs.hotkeys import double_hotkeys
from configs.languages_mapping import english_to_russian_mapping


def on_press(key: Key | KeyCode) -> None:
    try:
        print(key.name)
    except AttributeError:
        current_language = get_current_language_hash()

        if current_language == '0x419':
            print(english_to_russian_mapping[str(key.char)])
        else:
            print(str(key.char))


def on_move(x: int, y: int) -> None:
    print('Pointer moved to {0}'.format(
        (x, y)))


def on_click(x: int, y: int, button: Button, pressed: bool) -> None:
    print('{0} at {1}, on button: {2}'.format(
        'Pressed' if pressed else 'Released',
        (x, y),
        button))


def on_scroll(x: int, y: int, dx: int, dy: int) -> None:
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))


def save_clipboard_content(clipboard_content: str, path: str = 'clipboard.txt') -> None:
    with open(path, 'a') as file:
        file.write(clipboard_content + '\n')


def get_current_language_hash() -> str:
    user32 = ctypes.WinDLL('user32.dll', use_last_error=True)
    current_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(current_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2 ** 16 - 1)
    return hex(lid)


def main():
    for shortcut, name in double_hotkeys:
        keyboard.add_hotkey(shortcut, lambda shortcut_name: print(shortcut_name), args=(name,))

    clipboard_tracker = ClipboardTracker(save_clipboard_content)
    try:
        clipboard_tracker.start()
    except KeyboardInterrupt:
        clipboard_tracker.stop()

    mouse_listener = pynput.mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)
    mouse_listener.start()

    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == '__main__':
    main()
