import json
import asyncio
import multiprocessing
from function_and_coroutine import print_loop_id


async def binance_client(q: multiprocessing.Queue):
    print(f'binance_client with Queue: {id(q)}')
    q.put('42')
    await asyncio.sleep(1)


async def account_data_server():
    print('account_data_server')
    await asyncio.sleep(1)


async def routine1():
    while True:
        print('routine1')
        await asyncio.sleep(3)


async def routine2():
    while True:
        print('routine2')
        await asyncio.sleep(5)


def f1(q: multiprocessing.Queue):
    print_loop_id()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(binance_client(q))
    loop.run_until_complete(account_data_server())
    loop.create_task(routine1())
    loop.create_task(routine2())
    loop.run_forever()


async def processor(q: multiprocessing.Queue):
    while True:
        item = q.get()
        print(f'processor: {json.dumps(item)}')
        await asyncio.sleep(1)


async def market_data_server():
    print('market_data_server')
    await asyncio.sleep(1)


def f2(q: multiprocessing.Queue):
    print_loop_id()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(market_data_server())
    loop.create_task(processor(q))
    loop.run_forever()


def main():
    q = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=f1, args=(q,))
    p1.start()
    p2 = multiprocessing.Process(target=f2, args=(q,))
    p2.start()

    p1.join()
    p2.join()


if __name__ == '__main__':
    main()
