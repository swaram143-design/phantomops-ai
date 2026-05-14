from core.task_queue_v2 import (
    task_queue
)

from core.jarvis_orchestrator_v2 import (
    jarvis
)


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

            result = await jarvis.execute_goal(
                task
            )

            print(
                f"[Pipeline] Result: "
                f"{result}"
            )

            await task_queue.task_done()


execution_pipeline = ExecutionPipeline()