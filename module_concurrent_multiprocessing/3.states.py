import threading
import time
import random


def Thread_execution(i):
    print("Execution of Thread {} started\n".format(i))
    sleepTime = random.randint(1, 4)
    time.sleep(sleepTime)
    print("Execution of Thread {} finished".format(i))


if __name__ == "__main__":
    for i in range(4):
        thread = threading.Thread(target=Thread_execution, args=(i,))
        thread.start()
        print("Active Threads:", threading.enumerate())
