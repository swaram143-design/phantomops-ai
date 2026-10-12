import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


class SlowWorker(Worker):
    name = "slow"
    capabilities = {"research"}

    async def run(self, task):
        await asyncio.sleep(0.15)
        return WorkerResult(True, {"done": True})


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            mid = state.create_mission("lease loss")
            plan = {"goal": "lease loss", "steps": [{"capability": "research", "action": "research"}]}
            state.update(mid, "running", plan=plan, result={"next_step": 0, "context": {}, "results": [], "attempts": {}})
            owner = "owner-1"
            assert state.claim_mission(mid, owner, lease_seconds=0.05, statuses=("running",))

            workers = WorkerRegistry()
            workers.register(SlowWorker())
            runtime = JarvisRuntime(
                state=StateStore(db.name),
                workers=workers,
                permissions=PermissionEngine("WORK"),
            )

            result = await runtime._run_owned(mid, "lease loss", plan, {}, owner, start_index=0)
            assert result["status"] == "lease_lost"
            mission = state.get_mission(mid)
            assert mission["status"] == "running"
            assert mission["result"] is not None

    asyncio.run(run())
    print("JARVIS-NEXT LEASE LOSS CONTRACT OK")


if __name__ == "__main__":
    main()
