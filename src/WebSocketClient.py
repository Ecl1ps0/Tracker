import websockets


class WebSocketClient:
    def __init__(self, url: str):
        self.url = url
        self.websocket = None

    async def connect(self) -> None:
        self.websocket = await websockets.connect(self.url)

    async def disconnect(self) -> None:
        await self.websocket.close()

    async def send_message(self, msg: str) -> str:
        await self.websocket.send(msg)
        response = await self.websocket.recv()
        return response
