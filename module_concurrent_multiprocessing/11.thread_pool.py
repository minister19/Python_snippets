from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep


def task(message):
    sleep(2)
    return message


def main():
    executor = ThreadPoolExecutor(5)
    future = executor.submit(task, ("Completed"))
    print(future.done())
    sleep(3)
    print(future.done())
    print(future.result())


if __name__ == '__main__':
    main()


values = [2, 3, 4, 5]


def square(n):
    return n * n


def main2():
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(square, values)
    for result in results:
        print(result)


if __name__ == '__main__':
    main2()
