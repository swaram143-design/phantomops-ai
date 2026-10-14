import asyncio
import json
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


class LateWorker(Worker):
    name = "late-worker"
    capabilities = {"research"}

    async def run(self, task):
        await asyncio.sleep(0.15)
        return WorkerResult(True, {"done": True})


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            mid = state.create_mission("late worker lease")
            plan = {
                "goal": "late worker lease",
                "steps": [{"capability": "research", "action": "research"}],
            }
            state.update(
                mid,
                "running",
                plan=plan,
                result={"next_step": 0, "context": {}, "results": [], "attempts": {}},
            )
            owner = "owner-1"
            assert state.claim_mission(mid, owner, lease_seconds=0.05, statuses=("running",))

            workers = WorkerRegistry()
            workers.register(LateWorker())
            runtime = JarvisRuntime(
                state=StateStore(db.name),
                workers=workers,
                permissions=PermissionEngine("WORK"),
            )

            result = await runtime._run_owned(mid, "late worker lease", plan, {}, owner, start_index=0)
            assert result["status"] == "lease_lost"

            mission = state.get_mission(mid)
            assert mission["status"] == "running"
            durable = json.loads(mission["result"])
            assert durable["next_step"] == 0
            assert durable["results"] == []

            events = state.conn.execute(
                "SELECT kind FROM events WHERE mission_id=? ORDER BY id", (mid,)
            ).fetchall()
            assert "step.completed" not in [row["kind"] for row in events]
            assert "worker.uncertain" not in [row["kind"] for row in events]

    asyncio.run(run())
    print("JARVIS-NEXT LATE WORKER LEASE CONTRACT OK")


if __name__ == "__main__":
    main()
