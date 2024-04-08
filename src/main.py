import asyncio

import keyboard
import requests

from ClipboardTracker import ClipboardTracker
from WebSocketClient import WebSocketClient
from configs.file_writers import save_to_report, save_clipboard_content
from configs.hotkeys import double_hotkeys
from configs.logger import get_logger
from loggers.KeyboardLogger import KeyboardLogger
from loggers.MouseLogger import MouseLogger


async def main():
    logger = get_logger(__name__)

    logger.info("Start tracking actions")
    for shortcut, name in double_hotkeys:
        keyboard.add_hotkey(shortcut,
                            lambda shortcut_name: save_to_report(shortcut_name, path=".\\report.txt"),
                            args=(name,))

    socket = WebSocketClient("ws://localhost:8080/connection/ws")
    await socket.connect()

    keyboard_logger = KeyboardLogger()

    mouse_logger = MouseLogger()

    loggers = [ClipboardTracker(save_clipboard_content), keyboard_logger.create_listener(), mouse_logger.create_listener()]

    try:
        start_resp = await socket.send_message("start")
        print(start_resp)
        logger.info(start_resp)

        for tracker in loggers:
            logger.info(f"Start {type(tracker).__name__}")
            tracker.start()

        logger.info("Clipboard, mouse and keyboard tracker have started")

        while True:
            await asyncio.sleep(1)

    except (KeyboardInterrupt, asyncio.CancelledError):
        for tracker in loggers:
            logger.info(f"Start {type(tracker).__name__}")
            tracker.stop()

        finish_resp = await socket.send_message("finish")
        print(finish_resp)
        logger.info(finish_resp)

        await socket.disconnect()

        logger.info("Stop tracking")

    json_data = {
        "files": [
            {"name": "logs", "data": open('logs.txt').read()},
            {"name": "report", "data": open('report.txt').read()},
            {"name": "clipboard", "data": open('clipboard.txt').read()},
        ]
    }

    requests.post("http://localhost:8080/connection/fileUpload", json=json_data)


if __name__ == '__main__':
    asyncio.run(main())
