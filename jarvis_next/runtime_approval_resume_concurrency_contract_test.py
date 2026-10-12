import asyncio
import tempfile
import threading

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore


class SlowSendWorker(Worker):
    name = "slow_send"
    capabilities = {"external_send"}

    def __init__(self):
        self.calls = 0
        self.lock = threading.Lock()

    async def run(self, task):
        with self.lock:
            self.calls += 1
        await asyncio.sleep(0.05)
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
    async def prepare(db, worker):
        state = StateStore(db)
        workers = WorkerRegistry()
        workers.register(worker)
        runtime = JarvisRuntime(state=state, workers=workers)
        runtime.planner = FixedPlanner()
        pending = await runtime.submit("send prepared message")
        assert pending["status"] == "awaiting_approval"
        return pending["approval_id"], pending["mission_id"]

    with tempfile.NamedTemporaryFile(suffix=".db") as db:
        worker = SlowSendWorker()
        approval_id, mission_id = asyncio.run(prepare(db.name, worker))
        barrier = threading.Barrier(2)
        results = []
        errors = []

        def approve():
            try:
                state = StateStore(db.name)
                workers = WorkerRegistry()
                workers.register(worker)
                runtime = JarvisRuntime(state=state, workers=workers)
                runtime.planner = FixedPlanner()
                barrier.wait()
                results.append(asyncio.run(runtime.resume(approval_id, approved=True)))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=approve) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert not errors, errors
        assert len(results) == 2
        statuses = [result["status"] for result in results]
        assert statuses.count("completed") == 1, results
        assert statuses.count("already_running") == 1, results
        assert worker.calls == 1, worker.calls

        state = StateStore(db.name)
        approval = state.get_approval(approval_id)
        mission = state.get_mission(mission_id)
        assert approval["status"] == "approved"
        assert mission["status"] == "completed"
        state.conn.close()

    print("runtime approval resume concurrency contract: PASS")


if __name__ == "__main__":
    main()
