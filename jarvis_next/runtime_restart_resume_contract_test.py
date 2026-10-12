import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .permissions import PermissionEngine
from .state import StateStore


class SendWorker(Worker):
    name = "send"
    capabilities = {"external_send"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(True, {"sent": True})


class FixedPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "external_send", "action": "external_send"}]}


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            first_state = StateStore(db.name)
            workers = WorkerRegistry()
            worker = SendWorker()
            workers.register(worker)

            first = JarvisRuntime(
                state=first_state,
                workers=workers,
                permissions=PermissionEngine("WORK"),
            )
            first.planner = FixedPlanner()

            pending = await first.submit("send the approved message")
            assert pending["status"] == "awaiting_approval"
            approval_id = pending["approval_id"]
            assert worker.calls == 0

            # Simulate a process restart by opening the same durable DB with a
            # new StateStore/runtime. The pending approval must be reused.
            second_state = StateStore(db.name)
            second = JarvisRuntime(
                state=second_state,
                workers=workers,
                permissions=PermissionEngine("WORK"),
            )
            resumed = await second.resume_mission(pending["mission_id"])
            assert resumed["status"] == "awaiting_approval"
            assert resumed["approval_id"] == approval_id
            assert worker.calls == 0

            completed = await second.resume(approval_id, approved=True)
            assert completed["status"] == "completed"
            assert worker.calls == 1

            # Reopening the runtime after completion must not execute the
            # already-completed side effect again.
            third = JarvisRuntime(
                state=StateStore(db.name),
                workers=workers,
                permissions=PermissionEngine("WORK"),
            )
            again = await third.resume_mission(pending["mission_id"])
            assert again["status"] == "completed"
            assert worker.calls == 1

    asyncio.run(run())
    print("JARVIS-NEXT RESTART RESUME CONTRACT OK")


if __name__ == "__main__":
    main()
