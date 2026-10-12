import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


class ReadWorker(Worker):
    name = "read_worker"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(True, {"value": 1})


class FixedPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "research", "action": "research"}]}


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            worker = ReadWorker()
            workers.register(worker)
            runtime = JarvisRuntime(
                state=state,
                workers=workers,
                permissions=PermissionEngine("OBSERVE"),
            )
            runtime.planner = FixedPlanner()

            blocked = await runtime.submit("research while observe-only")
            assert blocked["status"] == "blocked"
            assert worker.calls == 0

            resumed = await runtime.resume_mission(blocked["mission_id"])
            assert resumed["status"] == "blocked"
            assert worker.calls == 0, "blocked mission must not bypass permission policy"

            mission = state.get_mission(blocked["mission_id"])
            assert mission["status"] == "blocked"

    asyncio.run(run())
    print("JARVIS-NEXT BLOCKED RESUME CONTRACT OK")


if __name__ == "__main__":
    main()
