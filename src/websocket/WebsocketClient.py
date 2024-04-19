from websockets import WebSocketClientProtocol


class Client:
    def __init__(self, websocket_connection: WebSocketClientProtocol, ):
        self.websocket_connection = websocket_connection

    async def send_msg(self, msg: str) -> str:
        await self.websocket_connection.send(msg)
        return await self.websocket_connection.recv()
