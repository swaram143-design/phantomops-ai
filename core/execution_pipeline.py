from core.task_queue_v2 import (
    task_queue
)

from jarvis_next.govi_core import GoviCore


# Compatibility pipeline retained; mission execution is owned by GOVI.
govi = GoviCore()


class ExecutionPipeline:

    async def submit_goal(self, goal):

        await task_queue.add_task(goal)

    async def process_tasks(self):

        print(
            "[Pipeline] Processing started"
        )

        while True:

            task = await task_queue.get_task()

            print(
                f"[Pipeline] Executing: "
                f"{task}"
            )

            result = await govi.submit(
                task
            )

            print(
                f"[Pipeline] Result: "
                f"{result}"
            )

            await task_queue.task_done()


execution_pipeline = ExecutionPipeline()
