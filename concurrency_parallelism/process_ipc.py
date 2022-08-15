import time
import concurrent.futures
import multiprocessing


def f1(q: multiprocessing.Queue):
    for i in range(10):
        q.put([42, None, 'hello'])
        time.sleep(0.1)


def f2(q: multiprocessing.Queue):
    for i in range(10):
        item = q.get()
        print(item)
        time.sleep(0.01)


def main():
    start = time.time()
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=f1, args=(q,))
    p2 = multiprocessing.Process(target=f2, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print('Totalc time taken: {}'.format(time.time() - start))


# https://www.programminghunter.com/article/1997601723/
def main2():
    start = time.time()
    q = multiprocessing.Manager().Queue()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        future1 = pool.submit(f1, q)
        future2 = pool.submit(f2, q)
        print(future1.result(), future2.result())
    print('Totalc time taken: {}'.format(time.time() - start))


if __name__ == '__main__':
    main()
    main2()
