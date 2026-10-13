import asyncio
import json
import tempfile
from datetime import datetime, timezone

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore


class DatetimeWorker(Worker):
    name = "datetime-worker"
    capabilities = {"research"}

    async def run(self, task):
        return WorkerResult(
            True,
            data={
                "completed_at": datetime(2026, 10, 13, 5, 57, 0, tzinfo=timezone.utc),
                "nested": {"seen": datetime(2026, 10, 13, 5, 58, 0, tzinfo=timezone.utc)},
            },
        )


class FixedPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "research", "action": "research"}]}


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            workers.register(DatetimeWorker())

            runtime = JarvisRuntime(state=state, workers=workers)
            runtime.planner = FixedPlanner()
            input_context = {"requested_at": datetime(2026, 10, 13, 5, 56, 0, tzinfo=timezone.utc)}

            result = await runtime.submit("persist structured result", context=input_context)
            assert result["status"] == "completed"
            assert isinstance(result["context"]["requested_at"], str)
            assert isinstance(result["results"][0]["data"]["completed_at"], str)
            assert isinstance(result["results"][0]["data"]["nested"]["seen"], str)

            mission = state.get_mission(result["mission_id"])
            persisted = json.loads(mission["result"])
            assert persisted["context"] == result["context"]
            assert persisted["results"] == result["results"]

            restarted = StateStore(db.name)
            reloaded = json.loads(restarted.get_mission(result["mission_id"])["result"])
            assert reloaded == persisted

    asyncio.run(run())
    print("JARVIS-NEXT RESULT SERIALIZATION CONTRACT OK")


if __name__ == "__main__":
    main()
