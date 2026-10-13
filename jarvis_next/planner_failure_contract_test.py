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

        original_insert_event = state._insert_event

        def fail_planning_event(kind, payload, mid=None):
            if kind == "mission.planning_failed":
                raise RuntimeError("planning event write failed")
            return original_insert_event(kind, payload, mid)

        state._insert_event = fail_planning_event
        result = await runtime.submit("find revenue opportunities")
        mission = state.get_mission(result["mission_id"])
        assert mission["status"] == "queued"
        assert mission["plan"] is None
        assert mission["result"] is None
        assert state.conn.execute(
            "SELECT COUNT(*) FROM events WHERE mission_id=? AND kind='mission.planning_failed'",
            (result["mission_id"],),
        ).fetchone()[0] == 0

        state._insert_event = original_insert_event
        result = await runtime.submit("find revenue opportunities")
        assert result["status"] == "failed"
        assert result["error"] == "planner unavailable"

        mission = state.get_mission(result["mission_id"])
        assert mission["status"] == "failed"
        assert mission["plan"] is None
        persisted = json.loads(mission["result"])
        assert persisted["error"] == "planner unavailable"
        assert state.conn.execute(
            "SELECT COUNT(*) FROM events WHERE mission_id=? AND kind='mission.planning_failed'",
            (result["mission_id"],),
        ).fetchone()[0] == 1

        print("JARVIS-NEXT PLANNER FAILURE ATOMICITY OK")


if __name__ == "__main__":
    asyncio.run(run())
