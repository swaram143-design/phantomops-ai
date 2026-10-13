import asyncio
import json
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore


class UncertainWorker(Worker):
    name = "uncertain"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(
            False,
            error="external request outcome unknown after timeout",
            retryable=False,
            side_effect_uncertain=True,
        )


class FallbackWorker(Worker):
    name = "fallback"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(True, {"fallback": True})


class FixedPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "research", "action": "research"}]}


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            uncertain = UncertainWorker()
            fallback = FallbackWorker()
            workers.register(uncertain)
            workers.register(fallback)

            runtime = JarvisRuntime(state=state, workers=workers, max_retries=2, retry_delay=0)
            runtime.planner = FixedPlanner()
            result = await runtime.submit("research with uncertain external outcome")

            assert result["status"] == "failed"
            assert uncertain.calls == 1
            assert fallback.calls == 0, "uncertain external outcome must not fall back to another worker"
            mission = state.get_mission(result["mission_id"])
            persisted = json.loads(mission["result"])
            assert persisted["attempts"]["0:uncertain"] == 1
            assert persisted["results"][-1]["side_effect_uncertain"] is True

    asyncio.run(run())
    print("JARVIS-NEXT UNCERTAIN OUTCOME NO-FALLBACK CONTRACT OK")


if __name__ == "__main__":
    main()
