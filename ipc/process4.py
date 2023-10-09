import asyncio

# Define an asynchronous coroutine


async def my_coroutine():
    print("Start Coroutine")
    await asyncio.sleep(2)  # Simulate some asynchronous work
    print("Coroutine Completed")

# Create an event loop
loop = asyncio.get_event_loop()

# Use run_until_complete to run the coroutine until it completes
try:
    loop.run_until_complete(my_coroutine())
finally:
    loop.close()
