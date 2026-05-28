import asyncio
import time

async def fetch_data(id, delay):
    print(f"Task {id} started")

    await asyncio.sleep(delay)

    print(f"Task {id} completed")

    return f"Data from Task {id}"

async def main():

    results = await asyncio.gather(
        fetch_data(1, 3),
        fetch_data(2, 2),
        fetch_data(3, 1)
    )

    print("\nResults:")
    print(results)

if __name__ == "__main__":

    start = time.perf_counter()

    asyncio.run(main())

    end = time.perf_counter()

    print(f"\nTime Taken: {end-start:.2f} sec")