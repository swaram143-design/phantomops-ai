import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore


class FailingWorker(Worker):
    name = "unstable"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(False, error="temporary network timeout", retryable=True)


class FixedPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "research", "action": "research"}]}


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            worker = FailingWorker()
            workers.register(worker)

            runtime = JarvisRuntime(
                state=state,
                workers=workers,
                max_retries=2,
                retry_delay=0,
            )
            runtime.planner = FixedPlanner()

            result = await runtime.submit("research with retry exhaustion")
            assert result["status"] == "failed"
            assert worker.calls == 3, "max_retries=2 must allow initial attempt plus two retries"

            mission = state.get_mission(result["mission_id"])
            assert mission["status"] == "failed"
            persisted = __import__("json").loads(mission["result"])
            assert persisted["attempts"]["0:unstable"] == 3
            assert persisted["results"][-1]["status"] == "failed"
            assert persisted["results"][-1]["attempt"] == 3

            resumed = await runtime.resume_mission(result["mission_id"])
            assert resumed["status"] == "failed"
            assert worker.calls == 3, "failed mission must not silently re-execute after retry exhaustion"

    asyncio.run(run())
    print("JARVIS-NEXT TRUE RETRY EXHAUSTION CONTRACT OK")


if __name__ == "__main__":
    main()
