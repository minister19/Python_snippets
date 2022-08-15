import time
import multiprocessing


def child_process():
    print("PID of Child Process is: {}".format(multiprocessing.current_process().pid))


if __name__ == '__main__':
    print("PID of Main process is: {}".format(multiprocessing.current_process().pid))
    P = multiprocessing.Process(target=child_process)
    P.start()
    P.join()
