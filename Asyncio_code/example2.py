import asyncio
import time
from random import randint


async def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)
    print(f"done processing {param}.")
    return f"result of {param}"

async def main():
    task1=asyncio.create_task(fetch_data(1))
    task2= asyncio.create_task(fetch_data(2))

    result1 = await task1
    print("task is fully completed")

    result2  = await task2
    print("task is fully completed")
    return [result1, result2]

t1=time.perf_counter()

result = asyncio.run(main())


print(result)

t2=time.perf_counter()
print(f"total time taken {t2-t1} seconds")  