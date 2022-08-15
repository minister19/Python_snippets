import time
import multiprocessing


def child_process():
    print('Starting function')
    time.sleep(5)
    print('Finished function')


if __name__ == '__main__':
    p = multiprocessing.Process(target=child_process)
    p.start()
    time.sleep(1)
    print("Terminating Child Process")
    p.terminate()
    print("Child Process successfully terminated")
