import multiprocessing
import asyncio


async def modify_data(shared_data, notification_event):
    for i in range(5):
        # Modify the shared data
        shared_data.value = i

        # Trigger the notification event
        notification_event.set()
        await asyncio.sleep(2)


async def notify_process(shared_data, notification_event):
    while True:
        await notification_event.wait()
        notification_event.clear()
        print(f"Received notification. Shared data: {shared_data.value}")

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        shared_data = manager.Value('i', 0)
        notification_event = asyncio.Event()

        loop = asyncio.get_event_loop()

        # Create tasks for both modify_data and notify_process
        tasks = [
            loop.create_task(modify_data(shared_data, notification_event)),
            loop.create_task(notify_process(shared_data, notification_event)),
        ]

        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        except KeyboardInterrupt:
            pass
