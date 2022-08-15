import asyncio
from multiprocessing import Value

var2 = {'a': 1}
var3 = Value('d', 0.0)


async def main():
    lock = asyncio.Lock()

    async with lock:
        # access shared state
        global var
        var = 1
        var2['a'] += 1
        var3.value += 3.1415926

if __name__ == '__main__':
    global var
    var = 0
    print(var, var2, var3)
    asyncio.run(main())
    print(var, var2, var3)
