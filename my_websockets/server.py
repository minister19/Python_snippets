# ref: https://medium.com/better-programming/how-to-create-a-websocket-in-python-b68d65dbd549

import asyncio
import websockets
from websockets import WebSocketServerProtocol as WSP
from typing import Set, Callable


class WebSocketServer:
    def __init__(self, host: str, port: int, handle_message: Callable[[WSP, str], None]) -> None:
        self.host = host
        self.port = port
        self.handle_message = handle_message
        self.server = None
        self.clients: Set[WSP] = set()

    async def start(self) -> None:
        self.server = await websockets.serve(self._handle_client, self.host, self.port)

    async def stop(self) -> None:
        await self.server.wait_closed()

    async def _handle_client(self, client: WSP, path: str) -> None:
        self.clients.add(client)
        try:
            async for message in client:
                await self.handle_message(client, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(client)

    async def send(self, client: WSP, message: str) -> None:
        if client:
            await client.send(message)

    async def broadcast(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])


if __name__ == "__main__":
    async def handle_message(sender: WSP, message: str) -> None:
        print(sender, message)
        await sender.send(message)
        pass

    async def main() -> None:
        server = WebSocketServer("localhost", 6800, handle_message)
        await server.start()
        await asyncio.Future()  # run forever

    asyncio.run(main())
