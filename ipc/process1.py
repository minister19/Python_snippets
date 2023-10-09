import multiprocessing
import time


def modify_data(shared_data, notification_event):
    for i in range(5):
        # Modify the shared data
        shared_data.value = i

        # Trigger the notification event
        notification_event.set()
        time.sleep(2)


def notify_process(shared_data, notification_event):
    while True:
        # Wait for the notification event
        notification_event.wait()

        # Reset the event
        notification_event.clear()

        # React to the change in shared data
        print(f"Received notification. Shared data: {shared_data.value}")


if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        shared_data = manager.Value('i', 0)
        notification_event = manager.Event()

        process1 = multiprocessing.Process(target=modify_data, args=(shared_data, notification_event))
        process2 = multiprocessing.Process(target=notify_process, args=(shared_data, notification_event))

        process1.start()
        process2.start()

        process1.join()
        process2.join()
