import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore


class FailingWorker(Worker):
    name = "primary"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(False, error="permanent failure")


class BackupWorker(Worker):
    name = "backup"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(True, {"source": "backup"})


class FixedPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "research", "action": "research"}]}


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            primary = FailingWorker()
            backup = BackupWorker()
            workers.register(primary)
            workers.register(backup)

            runtime = JarvisRuntime(state=state, workers=workers, max_retries=0)
            runtime.planner = FixedPlanner()

            result = await runtime.submit("research with fallback")
            assert result["status"] == "completed"
            assert primary.calls == 1
            assert backup.calls == 1
            assert result["results"][0]["worker"] == "primary"
            assert result["results"][0]["status"] == "failed"
            assert result["results"][-1]["worker"] == "backup"
            assert result["results"][-1]["status"] == "completed"

    asyncio.run(run())
    print("JARVIS-NEXT FALLBACK CONTRACT OK")


if __name__ == "__main__":
    main()
