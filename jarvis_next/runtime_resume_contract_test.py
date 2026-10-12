import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore


class FakeWorker(Worker):
    name = "fake_research"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(True, {"value": self.calls})


class FixedPlanner:
    def plan(self, goal, context=None):
        return {
            "goal": goal,
            "steps": [
                {"capability": "research", "action": "research"},
            ],
        }


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            worker = FakeWorker()
            workers.register(worker)

            runtime = JarvisRuntime(state=state, workers=workers)
            runtime.planner = FixedPlanner()

            first = await runtime.submit("research the target")
            assert first["status"] == "completed"
            assert worker.calls == 1

            resumed = await runtime.resume_mission(first["mission_id"])
            assert resumed["status"] == "completed"
            assert worker.calls == 1, "completed mission must not execute again"

    asyncio.run(run())
    print("JARVIS-NEXT RESUME CONTRACT OK")


if __name__ == "__main__":
    main()
