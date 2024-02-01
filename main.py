import keyboard
import pynput

from pynput.keyboard import Key
from pynput.mouse import Button

from configs.hotkeys import double_hotkeys


def on_press(key: Key) -> None:
    try:
        print(key.name)
    except AttributeError:
        print(key)


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


def main():
    for shortcut, name in double_hotkeys:
        keyboard.add_hotkey(shortcut, lambda shortcut_name: print(shortcut_name), args=(name,))

    mouse_listener = pynput.mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)
    mouse_listener.start()

    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == '__main__':
    main()
