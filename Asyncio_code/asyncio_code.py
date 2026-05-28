# asyncio_demo.py
"""
Asyncio Examples: Coroutines, Tasks, and Futures
Demonstrates Python's asyncio for concurrent programming.
"""

import asyncio
import time
from random import randint

# ====================== COROUTINE EXAMPLES ======================

async def simple_coroutine():
    """Basic coroutine example"""
    print("Coroutine started")
    await asyncio.sleep(1)  # Non-blocking sleep
    print("Coroutine finished")
    return "Result"

async def fetch_data(url, delay):
    """Simulate fetching data from a URL"""
    print(f"Starting to fetch {url}")
    await asyncio.sleep(delay)  # Simulate network delay
    print(f"Finished fetching {url}")
    return f"Data from {url}"

async def process_data(data):
    """Process the fetched data"""
    print(f"Processing {data}")
    await asyncio.sleep(0.5)  # Simulate processing time
    return f"Processed: {data}"

# ====================== TASK EXAMPLES ======================

async def create_tasks():
    """Demonstrate creating and running tasks"""
    print("\n=== Task Examples ===")

    # Create tasks from coroutines
    task1 = asyncio.create_task(fetch_data("url1", 2))
    task2 = asyncio.create_task(fetch_data("url2", 1))
    task3 = asyncio.create_task(fetch_data("url3", 3))

    # Run tasks concurrently
    print("Tasks created, waiting for results...")
    result1 = await task1
    result2 = await task2
    result3 = await task3

    print(f"Results: {result1}, {result2}, {result3}")

async def task_with_timeout():
    """Demonstrate task with timeout"""
    print("\n=== Task with Timeout ===")

    try:
        # This will raise TimeoutError
        result = await asyncio.wait_for(fetch_data("slow_url", 5), timeout=2.0)
        print(f"Got result: {result}")
    except asyncio.TimeoutError:
        print("Task timed out!")

# ====================== FUTURE EXAMPLES ======================

async def set_future_result(future):
    """Set a result on a future after some work"""
    await asyncio.sleep(1)
    future.set_result("Future result is ready")

async def future_example():
    """Demonstrate using Futures"""
    print("\n=== Future Examples ===")

    # Create a Future
    future = asyncio.Future()

    # Schedule the future to be completed
    asyncio.create_task(set_future_result(future))

    # Wait for the future to complete
    print("Waiting for future result...")
    result = await future
    print(f"Future result: {result}")

async def future_with_exception():
    """Demonstrate future with exception"""
    print("\n=== Future with Exception ===")

    future = asyncio.Future()

    async def set_exception():
        await asyncio.sleep(1)
        future.set_exception(RuntimeError("Something went wrong!"))

    asyncio.create_task(set_exception())

    try:
        await future
    except RuntimeError as e:
        print(f"Caught exception: {e}")

# ====================== ADVANCED EXAMPLES ======================

async def gather_example():
    """Demonstrate asyncio.gather"""
    print("\n=== Gather Example ===")

    urls = [("url1", 1), ("url2", 2), ("url3", 0.5)]
    tasks = [fetch_data(url, delay) for url, delay in urls]

    # Run all tasks concurrently and gather results
    results = await asyncio.gather(*tasks)
    print(f"All results: {results}")

async def as_completed_example():
    """Demonstrate asyncio.as_completed"""
    print("\n=== As Completed Example ===")

    urls = [("url1", 2), ("url2", 1), ("url3", 3)]
    tasks = [fetch_data(url, delay) for url, delay in urls]

    # Process results as they complete
    for future in asyncio.as_completed(tasks):
        result = await future
        print(f"Got result: {result}")

async def producer_consumer():
    """Demonstrate producer-consumer pattern"""
    print("\n=== Producer-Consumer Example ===")

    async def producer(queue):
        for i in range(5):
            await asyncio.sleep(randint(1, 2))
            item = f"Item {i}"
            print(f"Produced {item}")
            await queue.put(item)
        await queue.put(None)  # Sentinel value

    async def consumer(queue):
        while True:
            item = await queue.get()
            if item is None:
                break
            print(f"Consumed {item}")
            await asyncio.sleep(0.5)

    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))

# ====================== MAIN FUNCTION ======================

async def main():
    """Run all examples"""
    print("=== Coroutine Examples ===")
    result = await simple_coroutine()
    print(f"Coroutine result: {result}")

    # Run all examples
    await create_tasks()
    await task_with_timeout()
    await future_example()
    await future_with_exception()
    await gather_example()
    await as_completed_example()
    await producer_consumer()

if __name__ == "__main__":
    # Measure execution time
    start_time = time.time()
    asyncio.run(main())
    print(f"\nTotal execution time: {time.time() - start_time:.2f} seconds")