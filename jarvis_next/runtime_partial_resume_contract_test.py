import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


class ResearchWorker(Worker):
    name = "research"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(True, {"research": "done"})


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
        return {
            "goal": goal,
            "steps": [
                {"capability": "research", "action": "research"},
                {"capability": "external_send", "action": "external_send"},
            ],
        }


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            research = ResearchWorker()
            send = SendWorker()
            workers.register(research)
            workers.register(send)

            first = JarvisRuntime(
                state=state,
                workers=workers,
                permissions=PermissionEngine("WORK"),
            )
            first.planner = FixedPlanner()

            pending = await first.submit("research then send")
            assert pending["status"] == "awaiting_approval"
            assert pending["step_index"] == 1
            assert research.calls == 1
            assert send.calls == 0
            assert len(pending["results"]) == 1

            second = JarvisRuntime(
                state=StateStore(db.name),
                workers=workers,
                permissions=PermissionEngine("WORK"),
            )
            resumed = await second.resume_mission(pending["mission_id"])
            assert resumed["status"] == "awaiting_approval"
            assert resumed["step_index"] == 1
            assert research.calls == 1, "completed earlier step must not execute again"
            assert send.calls == 0

            completed = await second.resume(pending["approval_id"], approved=True)
            assert completed["status"] == "completed"
            assert research.calls == 1
            assert send.calls == 1
            assert len(completed["results"]) == 2

    asyncio.run(run())
    print("JARVIS-NEXT PARTIAL RESUME CONTRACT OK")


if __name__ == "__main__":
    main()
