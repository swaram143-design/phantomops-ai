import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore


class RetryingWorker(Worker):
    name = "retrying"
    capabilities = {"research"}

    def __init__(self):
        self.calls = []

    async def run(self, task):
        self.calls.append((task["attempt"], task["idempotency_key"]))
        if task["attempt"] == 1:
            return WorkerResult(False, error="temporary network timeout", retryable=True)
        return WorkerResult(True, data={"summary": "ok"})


class FixedPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "research", "action": "research"}]}


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            worker = RetryingWorker()
            workers.register(worker)

            runtime = JarvisRuntime(state=state, workers=workers, max_retries=1, retry_delay=0)
            runtime.planner = FixedPlanner()

            result = await runtime.submit("research with stable idempotency key")
            assert result["status"] == "completed"
            assert [attempt for attempt, _ in worker.calls] == [1, 2]
            keys = [key for _, key in worker.calls]
            assert keys[0] == keys[1]
            assert keys[0].startswith(result["mission_id"] + ":0:retrying")

    asyncio.run(run())
    print("JARVIS-NEXT WORKER IDEMPOTENCY KEY CONTRACT OK")


if __name__ == "__main__":
    main()
