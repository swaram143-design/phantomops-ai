import asyncio

from core.execution_pipeline import (
    execution_pipeline
)


class RuntimeManager:

    def __init__(self):

        self.running = False

    async def start(self):

        self.running = True

        print(
            "[Runtime] PhantomOps runtime online"
        )

        asyncio.create_task(
            execution_pipeline.process_tasks()
        )

        while self.running:

            await asyncio.sleep(1)

    async def stop(self):

        self.running = False

        print(
            "[Runtime] Runtime stopped"
        )


runtime_manager = RuntimeManager()