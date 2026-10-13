import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


class CountingWorker(Worker):
    name = "counting"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(True, {"done": True})


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            mid = state.create_mission("expired lease guard")
            plan = {"goal": "expired lease guard", "steps": [{"capability": "research", "action": "research"}]}
            state.update(mid, "running", plan=plan, result={"next_step": 0, "context": {}, "results": [], "attempts": {}})
            owner = "owner-1"
            assert state.claim_mission(mid, owner, lease_seconds=0.01, statuses=("running",))
            await asyncio.sleep(0.03)

            worker = CountingWorker()
            workers = WorkerRegistry()
            workers.register(worker)
            runtime = JarvisRuntime(
                state=StateStore(db.name),
                workers=workers,
                permissions=PermissionEngine("WORK"),
            )

            result = await runtime._run_owned(mid, "expired lease guard", plan, {}, owner, start_index=0)
            assert result["status"] == "lease_lost"
            assert worker.calls == 0
            mission = state.get_mission(mid)
            assert mission["status"] == "running"
            assert json.loads(mission["result"])["next_step"] == 0

    import json
    asyncio.run(run())
    print("JARVIS-NEXT LEASE GUARD CONTRACT OK")


if __name__ == "__main__":
    main()
