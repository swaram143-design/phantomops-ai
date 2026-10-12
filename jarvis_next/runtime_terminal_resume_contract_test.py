import asyncio
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


class FailingWorker(Worker):
    name = "terminal_failure"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(False, error="permanent failure", retryable=False)


class SendWorker(Worker):
    name = "terminal_send"
    capabilities = {"external_send"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(True, {"sent": True})


class ResearchPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "research", "action": "research"}]}


class SendPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "external_send", "action": "external_send"}]}


def main():
    async def run():
        with tempfile.NamedTemporaryFile(suffix=".db") as db:
            state = StateStore(db.name)
            workers = WorkerRegistry()
            failing = FailingWorker()
            workers.register(failing)
            runtime = JarvisRuntime(state=state, workers=workers, max_retries=0)
            runtime.planner = ResearchPlanner()

            failed = await runtime.submit("run a permanently failing task")
            assert failed["status"] == "failed"
            assert failing.calls == 1

            resumed_failed = await runtime.resume_mission(failed["mission_id"])
            assert resumed_failed["status"] == "failed"
            assert failing.calls == 1, "failed mission must not execute again"

            second_state = StateStore(db.name)
            send_workers = WorkerRegistry()
            sender = SendWorker()
            send_workers.register(sender)
            sender_runtime = JarvisRuntime(
                state=second_state,
                workers=send_workers,
                permissions=PermissionEngine("WORK"),
            )
            sender_runtime.planner = SendPlanner()

            pending = await sender_runtime.submit("send the message")
            assert pending["status"] == "awaiting_approval"
            rejected = await sender_runtime.resume(pending["approval_id"], approved=False)
            assert rejected["status"] == "rejected"
            assert sender.calls == 0

            resumed_rejected = await sender_runtime.resume_mission(pending["mission_id"])
            assert resumed_rejected["status"] == "rejected"
            assert sender.calls == 0, "rejected mission must not execute again"

    asyncio.run(run())
    print("JARVIS-NEXT TERMINAL RESUME CONTRACT OK")


if __name__ == "__main__":
    main()
