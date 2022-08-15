import time
import requests
import aiohttp
import asyncio
import concurrent.futures


def print_loop_id():
    loop = asyncio.get_event_loop()
    print('loop id:', id(loop))


def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a process pool.
    return sum(i * i for i in range(10 ** 7))


def make_request():
    response = requests.get("https://httpbin.org/ip")
    print('Response status -> %d' % response.status_code)

    response_json = response.json()
    print('Response data -> %s' % response_json)

    return response_json


async def make_request_async():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://httpbin.org/ip") as response:
            print('Response status -> %d' % response.status)

            response_json = await response.json()
            print('Response data -> %s' % response_json)

            return response_json


def f1():
    cpu_bound()
    make_request()


def f2():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_request_async())
    # loop.run_forever()


async def f3():
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, make_request)


if __name__ == '__main__':
    start = time.time()
    f1()
    print('Total time taken: {}'.format(time.time() - start))
    f2()
    print('Total time taken: {}'.format(time.time() - start))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(f3())
    print('Total time taken: {}'.format(time.time() - start))
