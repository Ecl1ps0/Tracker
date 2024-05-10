import asyncio
import json

from websockets import WebSocketServerProtocol

from configs.logger import get_logger

logger = get_logger(__name__)


class WebsocketHandler:
    def __init__(self):
        self.start_event = asyncio.Event()
        self.end_event = asyncio.Event()
        self.websocket_message = None

    async def handler(self, websocket: WebSocketServerProtocol, path: str) -> None:
        async for message in websocket:
            try:
                msg = json.loads(message)
                self.websocket_message = msg
            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
                continue

            print(f"Received from client: {msg.get('Message')}")
            match msg.get('Message'):
                case "start":
                    self.start_event.set()
                case "stop":
                    self.end_event.set()
                    break

            await websocket.send(f"Message received by server: {message}")
