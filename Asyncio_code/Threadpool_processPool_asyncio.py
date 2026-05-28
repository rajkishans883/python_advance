import asyncio
from multiprocessing import pool
import time
from random import randint
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def fetch_data(param):
    print(f"Do something with {param}...",flush=True)
    time.sleep(param)
    print(f"done processing {param}.",flush=True)
    return f"result of {param}"

async def main():
    task1=asyncio.create_task(asyncio.to_thread(fetch_data, 1))
    task2= asyncio.create_task(asyncio.to_thread(fetch_data, 2))

    result1 = await task1
    print("thread is fully completed")

    result2  = await task2
    print("thread is fully completed")

    loop=asyncio.get_running_loop()

    with ProcessPoolExecutor() as executor:
        task1=loop.run_in_executor(executor, fetch_data, 1)
        task2= loop.run_in_executor(executor, fetch_data, 2)

        result1 = await task1
        print("process1 is fully completed")
        result2  = await task2
        print("process2 is fully completed")



    return [result1, result2]


if __name__ == "__main__":
    t1=time.perf_counter()

    result = asyncio.run(main())


    print(result)

    t2=time.perf_counter()
    print(f"total time taken {t2-t1} seconds")  