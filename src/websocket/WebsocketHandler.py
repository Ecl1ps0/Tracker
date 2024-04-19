import asyncio

from websockets import WebSocketServerProtocol


class WebsocketHandler:
    def __init__(self):
        self.start_event = asyncio.Event()
        self.end_event = asyncio.Event()

    async def handler(self, websocket: WebSocketServerProtocol, path: str) -> None:
        async for message in websocket:
            print(f"Received from client: {message}")
            match message:
                case "start":
                    self.start_event.set()
                case "stop":
                    self.end_event.set()
                    break

            await websocket.send(f"Message received by server: {message}")
