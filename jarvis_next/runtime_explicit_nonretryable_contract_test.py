import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore


class AmbiguousWorker(Worker):
    name = "ambiguous"
    capabilities = {"external_send"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(
            False,
            error="external request outcome unknown after timeout",
            retryable=False,
        )


class FixedPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "external_send", "action": "research"}]}


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            worker = AmbiguousWorker()
            workers.register(worker)

            runtime = JarvisRuntime(
                state=state,
                workers=workers,
                max_retries=3,
                retry_delay=0,
            )
            runtime.planner = FixedPlanner()

            result = await runtime.submit("send with ambiguous outcome")
            assert result["status"] == "failed"
            assert worker.calls == 1, "an explicitly nonretryable adapter result must not be retried"

            mission = state.get_mission(result["mission_id"])
            assert mission["status"] == "failed"
            persisted = __import__("json").loads(mission["result"])
            assert persisted["attempts"]["0:ambiguous"] == 1
            assert persisted["results"][-1]["status"] == "failed"
            assert "outcome unknown" in persisted["results"][-1]["error"]

    asyncio.run(run())
    print("JARVIS-NEXT EXPLICIT NONRETRYABLE CONTRACT OK")


if __name__ == "__main__":
    main()
