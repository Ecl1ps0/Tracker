import asyncio
import json

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

    while True:
        keyboard_logger = KeyboardLogger().create_listener()
        mouse_logger = MouseLogger().create_listener()
        clipboard_logger = ClipboardTracker(save_clipboard_content)

        loggers = [clipboard_logger, keyboard_logger, mouse_logger]

        loggers_handler = LoggerHandler(loggers, logger)

        async with (websockets.connect("ws://localhost:8080/connection/ws") as socket,
                    websockets.serve(websocket_handler.handler, "localhost", 8001)):
            websocket_client = Client(socket)

            await websocket_handler.start_event.wait()

            start_data = {
                "StudentTaskID": websocket_handler.websocket_message.get("StudentTaskID"),
                "Message": "start"
            }

            start_resp = await websocket_client.send_msg(json.dumps(start_data))
            print(start_resp)
            logger.info(start_resp)

            loggers_handler.start_tracking()

            await websocket_handler.end_event.wait()
            websocket_handler.start_event.clear()
            websocket_handler.end_event.clear()

            loggers_handler.stop_tracking()

            finish_data = {
                "StudentTaskID": websocket_handler.websocket_message.get("StudentTaskID"),
                "Message": "finish"
            }

            finish_resp = await websocket_client.send_msg(json.dumps(finish_data))
            print(finish_resp)
            logger.info(finish_resp)

            logger.info("Stop tracking")

        json_data = {
            "StudentTaskID": websocket_handler.websocket_message.get("StudentTaskID"),
            "Files": [
                {"name": "logs", "data": open('logs.txt').read()},
                {"name": "report", "data": open('report.txt').read()},
                {"name": "clipboard", "data": open('clipboard.txt').read()},
            ]
        }

        requests.post("http://localhost:8080/api/report/createReport",
                      json=json_data,
                      headers={"Authorization": f"Bearer {client.token}"})


if __name__ == '__main__':
    asyncio.run(main())
