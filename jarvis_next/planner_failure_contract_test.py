import asyncio
import json
import tempfile

from .runtime import JarvisRuntime
from .state import StateStore


class FailingPlanner:
    def plan(self, goal, context):
        raise RuntimeError("planner unavailable")


async def run():
    with tempfile.TemporaryDirectory() as tmp:
        state = StateStore(f"{tmp}/state.db")
        runtime = JarvisRuntime(state=state)
        runtime.planner = FailingPlanner()

        result = await runtime.submit("find revenue opportunities")
        assert result["status"] == "failed"
        assert result["error"] == "planner unavailable"

        mission = state.get_mission(result["mission_id"])
        assert mission["status"] == "failed"
        assert mission["plan"] is None
        persisted = json.loads(mission["result"])
        assert persisted["error"] == "planner unavailable"

        print("JARVIS-NEXT PLANNER FAILURE OK")


if __name__ == "__main__":
    asyncio.run(run())
