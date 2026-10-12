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

            result = await runtime.submit("send the prepared message")

            assert result["status"] == "awaiting_approval"
            assert result["step_index"] == 0
            assert result["step"]["action"] == "external_send"
            assert sender.calls == 0, "runtime permission gate must block the worker before approval"

            approval = state.get_approval(result["approval_id"])
            assert approval["status"] == "pending"
            assert approval["action"] == "external_send"

            resumed = await runtime.resume(result["approval_id"], approved=True)
            assert resumed["status"] == "completed"
            assert sender.calls == 1, "approved external action must execute exactly once"

            approval = state.get_approval(result["approval_id"])
            assert approval["status"] == "approved"

    asyncio.run(run())
    print("JARVIS-NEXT RUNTIME PERMISSION GATE OK")


if __name__ == "__main__":
    main()
