import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .permissions import PermissionEngine
from .state import StateStore


class BlockingWorker(Worker):
    name = "blocking"
    capabilities = {"research"}

    def __init__(self, started, release):
        self.started = started
        self.release = release
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        self.started.set()
        await self.release.wait()
        return WorkerResult(True, {"done": True})


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            mid = state.create_mission("resume concurrently")
            plan = {"goal": "resume concurrently", "steps": [{"capability": "research", "action": "research"}]}
            state.update(mid, "running", plan=plan, result={"next_step": 0, "context": {}, "results": [], "attempts": {}})

            started = asyncio.Event()
            release = asyncio.Event()
            worker = BlockingWorker(started, release)
            workers = WorkerRegistry()
            workers.register(worker)

            first = JarvisRuntime(
                state=StateStore(db.name),
                workers=workers,
                permissions=PermissionEngine("WORK"),
            )
            second = JarvisRuntime(
                state=StateStore(db.name),
                workers=workers,
                permissions=PermissionEngine("WORK"),
            )

            first_task = asyncio.create_task(first.resume_mission(mid))
            await started.wait()
            second_result = await second.resume_mission(mid)
            assert second_result["status"] == "already_running"
            assert worker.calls == 1

            release.set()
            first_result = await first_task
            assert first_result["status"] == "completed"
            assert worker.calls == 1

    asyncio.run(run())
    print("JARVIS-NEXT CONCURRENT RESUME CONTRACT OK")


if __name__ == "__main__":
    main()
