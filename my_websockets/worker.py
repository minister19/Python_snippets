import asyncio
import json
import queue
import threading
import time

from client import WebSocketClient


# Chat: Python WebSocketServer in threading.Thread
# Chat: Can a Python threading.Event set twice?
def worker_ws_client_recv(event: threading.Event, ws_client: WebSocketClient) -> None:
    # Do some work
    while not event.is_set():
        # Continue working
        try:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(ws_client.connect())
            loop.run_until_complete(ws_client.receive())
        except Exception as e:
            print(f'worker_ws_client_recv error: {e}')


def worker_ws_client_send(event: threading.Event, ws_client: WebSocketClient, q: queue.Queue) -> None:
    while not event.is_set():
        try:
            while not ws_client or not ws_client.connected:
                time.sleep(1)
            loop = asyncio.new_event_loop()
            while True:
                item = q.get()
                loop.run_until_complete(ws_client.send(f'{item}'))
        except Exception as e:
            print(f'worker_ws_client_send error: {json.dumps(e)}')


def create_thread(ws_client: WebSocketClient, q: queue.Queue) -> None:
    try:
        event = threading.Event()
        recv_thread = threading.Thread(target=worker_ws_client_recv, args=(event, ws_client))
        send_thread = threading.Thread(target=worker_ws_client_send, args=(event, ws_client, q))
        return event, recv_thread, send_thread
    except Exception as e:
        print(f'create_thread error: {e}')
