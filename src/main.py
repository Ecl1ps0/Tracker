import asyncio
import json

import requests
import websockets

from ClipboardTracker import ClipboardTracker
from Login import Login
from TrafficTracer import TrafficTracer
from loggers.LoggerHandler import LoggerHandler
from websocket.WebsocketClient import Client
from websocket.WebsocketHandler import WebsocketHandler
from configs.file_writers import save_to_report, save_clipboard_content, clear_temp
from configs.hotkeys import HotkeyManager
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

    hotkey_manager = HotkeyManager()
    hotkey_manager.register_hotkeys()

    while True:
        keyboard_logger = KeyboardLogger()
        mouse_logger = MouseLogger()
        clipboard_logger = ClipboardTracker(save_clipboard_content)

        loggers = [clipboard_logger, keyboard_logger.create_listener(), mouse_logger.create_listener()]

        loggers_handler = LoggerHandler(loggers, logger)

        tracker = TrafficTracer()
        tracker.start_track()

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

            save_to_report(f"The final number of keystrokes: {keyboard_logger.num_of_keystrokes}")
            save_to_report(f"The number of function keys: {keyboard_logger.num_of_func_keys}")
            save_to_report(f"The number of internet traffic: {len(tracker.packets)}")
            hotkey_manager.save_hotkey_counts()

            loggers_handler.stop_tracking()

            finish_data = {
                "StudentTaskID": websocket_handler.websocket_message.get("StudentTaskID"),
                "Message": "finish"
            }

            finish_resp = await websocket_client.send_msg(json.dumps(finish_data))
            print(finish_resp)
            logger.info(finish_resp)

            logger.info("Stop tracking")
            tracker.stop_track()

        report_files = ["logs", "report", "clipboard"]
        json_data = {
            "StudentTaskID": websocket_handler.websocket_message.get("StudentTaskID"),
            "Files": [{"name": file, "data": open(f'.\\temp\\{file}.txt').read()} for file in report_files]
        }

        requests.post("http://localhost:8080/api/reports/createReport",
                      json=json_data,
                      headers={"Authorization": f"Bearer {client.token}"})

        clear_temp()


if __name__ == '__main__':
    asyncio.run(main())
