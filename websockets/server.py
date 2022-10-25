# ref: https://medium.com/better-programming/how-to-create-a-websocket-in-python-b68d65dbd549

import asyncio
import websockets
from websockets import WebSocketServerProtocol as WSP


class WebSocketServer:
    def __init__(self, host="0.0.0.0", port=6801) -> None:
        self.clients = set()
        self.host = host
        self.port = port
        self.onmessage_callback = None

    async def register(self, ws: WSP) -> None:
        self.clients.add(ws)

    async def unregister(self, ws: WSP) -> None:
        self.clients.remove(ws)

    async def send_to_clients(self, message: str) -> None:
        for ws in self.clients:
            try:
                await ws.send(message)
            except Exception as e:
                await self.unregister(ws)

    async def send_to_client(self, ws: WSP, message: str) -> None:
        if ws in self.clients:
            try:
                await ws.send(message)
            except Exception as e:
                await self.unregister(ws)

    async def ws_handler(self, ws: WSP, uri: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        except Exception as e:
            print(e)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WSP) -> None:
        async for message in ws:
            if self.onmessage_callback:
                await self.onmessage_callback(ws, message)

    def initialize(self, host, port, callback):
        self.host = host
        self.port = port
        self.onmessage_callback = callback

    def serve(self):
        return websockets.serve(self.ws_handler, self.host, self.port)


wsserver = WebSocketServer()

if __name__ == '__main__':
    wsserver = WebSocketServer()
    wsserver.initialize('localhost', 6801, None)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wsserver.serve())
    loop.run_forever()
