import asyncio


class TaskQueue:

    def __init__(self):

        self.queue = asyncio.Queue()

    async def add_task(self, task):

        await self.queue.put(task)

        print(
            f"[Queue] Task added: "
            f"{task}"
        )

    async def get_task(self):

        task = await self.queue.get()

        return task

    async def task_done(self):

        self.queue.task_done()


task_queue = TaskQueue()