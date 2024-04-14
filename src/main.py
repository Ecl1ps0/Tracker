import asyncio

import requests
import websockets
from websockets import WebSocketServerProtocol

from ClipboardTracker import ClipboardTracker
from Login import Login
from configs.file_writers import save_clipboard_content
from configs.hotkeys import register_hotkeys
from configs.logger import get_logger
from loggers.KeyboardLogger import KeyboardLogger
from loggers.MouseLogger import MouseLogger


async def handler(websocket: WebSocketServerProtocol, path: str) -> None:
    async for message in websocket:
        print(f"Received from client: {message}")
        await websocket.send("Message received by server")


async def main():
    logger = get_logger(__name__)

    client = Login()
    client.start_login()

    logger.info("Successfully logged in!")
    logger.info("Start tracking actions")
    register_hotkeys()

    async with (websockets.connect("ws://localhost:8080/connection/ws") as socket,
                websockets.serve(handler, "localhost", 8001) as server):
        keyboard_logger = KeyboardLogger()
        mouse_logger = MouseLogger()

        loggers = [ClipboardTracker(save_clipboard_content), keyboard_logger.create_listener(),
                   mouse_logger.create_listener()]

        try:
            await socket.send("start")
            start_resp = await socket.recv()
            print(start_resp)
            logger.info(start_resp)

            for tracker in loggers:
                logger.info(f"Start {type(tracker).__name__}")
                tracker.start()

            await asyncio.Future()

        except asyncio.CancelledError:
            for tracker in loggers:
                logger.info(f"Stop {type(tracker).__name__}")
                tracker.stop()

            await socket.send("finish")
            finish_resp = await socket.recv()
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
