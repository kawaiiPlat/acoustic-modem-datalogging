import asyncio

async def task(name, work_queue):
    while not work_queue.empty():
        delay = await work_queue.get()
        print(f"Task {name} running")
        await asyncio.sleep(delay)

async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for work in [3,3,3,3]:
        await work_queue.put(work)

    # Run the tasks
    await asyncio.gather(
        asyncio.create_task(task("One", work_queue)),
        asyncio.create_task(task("Two", work_queue)),
    )

if __name__ == "__main__":
    asyncio.run(main())