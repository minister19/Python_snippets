import time
import queue
import threading
import concurrent.futures


def f1(q: queue.Queue):
    for i in range(10):
        q.put([42, None, 'hello'])
        time.sleep(0.1)


def f2(q: queue.Queue):
    for i in range(10):
        item = q.get()
        print(item)
        time.sleep(0.01)


def main():
    start = time.time()
    q = queue.Queue()
    t1 = threading.Thread(target=f1, args=(q,))
    t2 = threading.Thread(target=f2, args=(q,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('Totalc time taken: {}'.format(time.time() - start))


def main2():
    start = time.time()
    q = queue.Queue()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        future1 = pool.submit(f1, q)
        future2 = pool.submit(f2, q)
        print(future1.result(), future2.result())
    print('Totalc time taken: {}'.format(time.time() - start))


if __name__ == '__main__':
    main()
    main2()
