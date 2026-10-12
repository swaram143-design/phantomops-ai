import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore


class FakeSendWorker(Worker):
    name = "fake_send"
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
                {"capability": "external_send", "action": "external_send"}
            ],
        }


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            sender = FakeSendWorker()
            workers.register(sender)

            runtime = JarvisRuntime(state=state, workers=workers)
            runtime.planner = FixedPlanner()

            pending = await runtime.submit("send the prepared message")
            assert pending["status"] == "awaiting_approval"
            approval_id = pending["approval_id"]
            assert sender.calls == 0

            rejected = await runtime.resume(approval_id, approved=False)
            assert rejected["status"] == "rejected"
            assert rejected["approval_id"] == approval_id
            assert sender.calls == 0, "rejected external action must never execute"

            approval = state.get_approval(approval_id)
            assert approval["status"] == "rejected"
            mission = state.get_mission(pending["mission_id"])
            assert mission["status"] == "rejected"

            repeated = await runtime.resume(approval_id, approved=True)
            assert repeated["status"] == "rejected"
            assert sender.calls == 0, "resolved approval must be idempotent"

    asyncio.run(run())
    print("JARVIS-NEXT APPROVAL REJECTION OK")


if __name__ == "__main__":
    main()
