import threading
import queue
import random
import time


print('FIFO Queue-------------')


def myFIFOQueue(queue: queue.Queue):
    while not queue.empty():
        item = queue.get()
        if item is None:
            break
        print("{} removed {} from the queue".format(threading.current_thread(), item))
        queue.task_done()
        time.sleep(1)


threads = []
q = queue.Queue()
for i in range(5):
    q.put(i)
for i in range(4):
    thread = threading.Thread(target=myFIFOQueue, args=(q,))
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()

print('LIFO Queue-------------')


def myLIFOQueue(queue: queue.LifoQueue):
    while not queue.empty():
        item = queue.get()
        if item is None:
            break
        print("{} removed {} from the queue".format(threading.current_thread(), item))
        queue.task_done()
        time.sleep(1)


threads = []
q = queue.LifoQueue()
for i in range(5):
    q.put(i)
for i in range(4):
    thread = threading.Thread(target=myLIFOQueue, args=(q,))
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()


print('Priority Queue---------')


def myPriorityQueue(queue: queue.PriorityQueue):
    while not queue.empty():
        item = queue.get()
        if item is None:
            break
        print("{} removed {} from the queue".format(threading.current_thread(), item))
        queue.task_done()
        time.sleep(1)


threads = []
q = queue.PriorityQueue()
for i in range(5):
    q.put(i, 1)

for i in range(5):
    q.put(i, 1)

for i in range(2):
    thread = threading.Thread(target=myPriorityQueue, args=(q,))
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
