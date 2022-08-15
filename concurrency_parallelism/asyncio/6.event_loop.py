import asyncio


def hello_world():
    """A callback to print 'Hello World' and stop the event loop"""
    print('Hello World')


def hello_world2(loop):
    """A callback to print 'Hello World' and stop the event loop"""
    print('Hello World')
    loop.stop()


async def hello_world3():
    print('Hello World')
    await asyncio.sleep(3)
    print('Hello World')


loop = asyncio.get_event_loop()

# Schedule a call to hello_world()
loop.call_soon(hello_world)
loop.call_later(5, hello_world2, loop)
loop.run_until_complete(hello_world3())
x = 1
print(x)

# Blocking call interrupted by loop.stop()
try:
    loop.run_forever()
finally:
    loop.close()
