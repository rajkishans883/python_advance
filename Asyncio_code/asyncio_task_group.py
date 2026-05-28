import asyncio

async def fetch_data(id, delay):

    print(f"Task {id} started")

    await asyncio.sleep(delay)

    print(f"Task {id} completed")

    return id

async def main():

    async with asyncio.TaskGroup() as tg:

        tg.create_task(fetch_data(1, 3))
        tg.create_task(fetch_data(2, 2))
        tg.create_task(fetch_data(3, 1))

    print("All tasks finished")

asyncio.run(main())























# import asyncio

# async def worker(name, delay):
#     print(f"{name} started")

#     await asyncio.sleep(delay)

#     print(f"{name} finished")

#     return name

# async def main():

#     task1 = asyncio.create_task(worker("A", 3))
#     task2 = asyncio.create_task(worker("B", 2))
#     task3 = asyncio.create_task(worker("C", 1))

#     results = await asyncio.gather(
#         task1,
#         task2,
#         task3
#     )

#     print(results)

# asyncio.run(main())