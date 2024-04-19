import asyncio

import requests
import websockets

from ClipboardTracker import ClipboardTracker
from Login import Login
from loggers.LoggerHandler import LoggerHandler
from websocket.WebsocketClient import Client
from websocket.WebsocketHandler import WebsocketHandler
from configs.file_writers import save_clipboard_content
from configs.hotkeys import register_hotkeys
from configs.logger import get_logger
from loggers.KeyboardLogger import KeyboardLogger
from loggers.MouseLogger import MouseLogger


async def main():
    logger = get_logger(__name__)

    client = Login()
    client.start_login()

    websocket_handler = WebsocketHandler()

    logger.info("Successfully logged in!")
    logger.info("Start tracking actions")
    register_hotkeys()

    keyboard_logger = KeyboardLogger().create_listener()
    mouse_logger = MouseLogger().create_listener()
    clipboard_logger = ClipboardTracker(save_clipboard_content)

    loggers = [clipboard_logger, keyboard_logger, mouse_logger]

    loggers_handler = LoggerHandler(loggers, logger)

    async with (websockets.connect("ws://localhost:8080/connection/ws") as socket,
                websockets.serve(websocket_handler.handler, "localhost", 8001)):
        client = Client(socket)

        await websocket_handler.start_event.wait()

        start_resp = await client.send_msg("start")
        print(start_resp)
        logger.info(start_resp)

        loggers_handler.start_tracking()

        await websocket_handler.end_event.wait()

        loggers_handler.stop_tracking()

        finish_resp = await client.send_msg("finish")
        print(finish_resp)
        logger.info(finish_resp)

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
