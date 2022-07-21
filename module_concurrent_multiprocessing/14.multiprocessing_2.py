import time
import multiprocessing


def non_daemon_process():
    print("starting my Process")
    time.sleep(3)
    print("ending my Process")


def daemon_process():
    while True:
        print("Hello")
        time.sleep(1)


if __name__ == '__main__':
    dp = multiprocessing.Process(target=daemon_process)
    dp.daemon = True
    dp.start()
    ndp = multiprocessing.Process(target=non_daemon_process)
    ndp.daemon = False
    ndp.start()
