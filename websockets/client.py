import json
import websockets
import asyncio


async def WSSClient():
    uri = "ws://localhost:6801"
    async with websockets.connect(uri) as websocket:
        msg = json.dumps({'a': 1})
        await websocket.send(msg)

        msg = 'history_15m_1000'
        await websocket.send(msg)

        for _ in range(1000):
            greeting = await websocket.recv()
            print(f"<<< {greeting}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(WSSClient())
