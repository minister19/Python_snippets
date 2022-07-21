import time
import concurrent.futures

value = [100000000, 200000000]


def counting(n):
    start = time.time()
    while n > 0:
        n -= 1
    return time.time() - start


def main():
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(5) as executor:
        for number, time_taken in zip(value, executor.map(counting, value)):
            print('Start: {} Time taken: {}'.format(number, time_taken))
    print('Total time taken: {}'.format(time.time() - start))


if __name__ == '__main__':
    main()


value = [100000000, 200000000]


def counting(n):
    start = time.time()
    while n > 0:
        n -= 1
    return time.time() - start


def main2():
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(5) as executor:
        for number, time_taken in zip(value, executor.map(counting, value)):
            print('Start: {} Time taken: {}'.format(number, time_taken))
    print('Total time taken: {}'.format(time.time() - start))


if __name__ == '__main__':
    main2()
