import time

from pynput import keyboard
from pynput.keyboard import Key


def on_press(key: Key) -> None:
    try:
        print(key.value, " ", key.name)
    except AttributeError:
        print("Special key: ", key)


def main():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    time.sleep(1000)


if __name__ == '__main__':
    main()
