import asyncio
import websockets
from typing import Callable


class WebSocketClient:
    def __init__(self, uri: str, on_message: Callable[[str], None]) -> None:
        self.uri = uri
        self.on_message = on_message
        self.websocket = None
        self.connected = False

    async def connect(self) -> None:
        self.websocket = await websockets.connect(self.uri)
        self.connected = True

    async def disconnect(self) -> None:
        await self.websocket.close()
        self.connected = False

    async def send(self, message: str) -> None:
        await self.websocket.send(message)

    async def receive(self) -> None:
        async for message in self.websocket:
            if self.on_message:
                await self.on_message(message)

    async def receiveOne(self) -> None:
        message = await self.websocket.recv()
        if self.on_message:
            await self.on_message(message)


if __name__ == "__main__":
    async def main() -> None:
        async def on_message(message: str) -> None:
            print(message)

        client = WebSocketClient("ws://localhost:6101", on_message)
        await client.connect()

        message = input("> ")
        await client.send(message)
        await client.receiveOne()

        # await client.receive()

        await client.disconnect()

    asyncio.run(main())
