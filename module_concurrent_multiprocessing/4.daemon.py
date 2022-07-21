import threading
import time


def nondaemonThread():
    print("starting my thread")
    time.sleep(3)
    print("ending my thread")


def daemonThread():
    while True:
        print("Hello")
        time.sleep(2)


if __name__ == "__main__":
    dp = threading.Thread(target=daemonThread)
    dp.setDaemon(True)
    dp.start()
    ndp = threading.Thread(target=nondaemonThread)
    ndp.start()
