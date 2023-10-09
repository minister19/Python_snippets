import multiprocessing


def producer(shared_queue):
    for item in range(5):
        shared_queue.put(f"Item {item}")


def consumer(shared_queue):
    while True:
        item = shared_queue.get()
        if item == 'STOP':
            break
        print(f"Consumer received: {item}")


if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        shared_queue = manager.Queue()

        producer_process = multiprocessing.Process(target=producer, args=(shared_queue,))
        consumer_process = multiprocessing.Process(target=consumer, args=(shared_queue,))

        producer_process.start()
        consumer_process.start()

        producer_process.join()

        # Signal the consumer to stop
        shared_queue.put('STOP')

        consumer_process.join()
