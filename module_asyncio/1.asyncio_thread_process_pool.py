import time
import asyncio
import concurrent.futures


def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open(f'{__file__}/../1.data', 'rb') as f:
        return f.read(100)


async def test1():
    await asyncio.sleep(1)
    blocking_io()


def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10 ** 7))


async def main():
    loop = asyncio.get_running_loop()

    # Options:

    # 1. Run in the default loop's executor:
    start = time.time()
    result = await loop.run_in_executor(None, blocking_io)
    print('default thread pool', result)
    print('Total time taken: {}'.format(time.time() - start))

    # 2. Run in a custom thread pool:
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_io)
        print('custom thread pool', result)
    print('Total time taken: {}'.format(time.time() - start))

    # 3. Run in a custom process pool:
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_bound)
        print('custom process pool', result)
    print('Total time taken: {}'.format(time.time() - start))

if __name__ == '__main__':
    asyncio.run(main())
