# ref: https://medium.com/better-programming/how-to-create-a-websocket-in-python-b68d65dbd549

import asyncio
import threading
import websockets
from websockets import WebSocketServerProtocol as WSP
from typing import Set

class WebSocketServer:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.server = None
        self.clients: Set[WSP] = set()

    async def start(self) -> None:
        self.server = await websockets.serve(self.handle_client, self.host, self.port)

    async def stop(self) -> None:
        await self.server.wait_closed()

    async def handle_client(self, websocket: WSP, path: str) -> None:
        self.clients.add(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)

    async def broadcast(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def handle_message(self, sender: WSP, message: str) -> None:
        print(sender, message)
        await sender.send(message)

# Chat: Python WebSocketServer in threading.Thread
# Chat: Can a Python threading.Event set twice?
def worker(event):
    # Do some work
    server = WebSocketServer("localhost", 1879)
    while not event.is_set():
        # Continue working
        loop = asyncio.new_event_loop()
        loop.run_until_complete(server.start())
        loop.run_forever()

def create_thread():
    event = threading.Event()
    thread = threading.Thread(target=worker, args=(event,))
    return event, thread

if __name__ == "__main__":
    async def main() -> None:
        server = WebSocketServer("localhost", 1879)
        await server.start()
        await asyncio.Future()  # run forever

    asyncio.run(main())
