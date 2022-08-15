import time
import asyncio
import concurrent.futures


def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open(f'{__file__}/../1.data', 'rb') as f:
        return f.read(100)


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

    # 1. Run in the default loop's executor:
    start = time.time()
    result = await loop.run_in_executor(None, cpu_bound)
    result = await loop.run_in_executor(None, cpu_bound)
    print('default thread pool', result)
    print('Total time taken: {}'.format(time.time() - start))

    # 2. Run in a custom thread pool:
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        t1 = loop.run_in_executor(pool, cpu_bound)
        t2 = loop.run_in_executor(pool, cpu_bound)
        # result = await loop.run_in_executor(pool, cpu_bound)
        result = await asyncio.gather(t1, t2)
        print('custom thread pool', result)
    print('Total time taken: {}'.format(time.time() - start))

    # 3. Run in a custom process pool:
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        t1 = loop.run_in_executor(pool, cpu_bound)
        t2 = loop.run_in_executor(pool, cpu_bound)
        # result = await loop.run_in_executor(pool, cpu_bound)
        result = await asyncio.gather(t1, t2)
        print('custom process pool', result)
    print('Total time taken: {}'.format(time.time() - start))

if __name__ == '__main__':
    asyncio.run(main())
