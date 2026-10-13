import asyncio
import json
import tempfile
from concurrent.futures import ThreadPoolExecutor

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore
from .uncertain_reconciliation import reconcile_uncertain


class UncertainThenSuccess(Worker):
    name = "uncertain_then_success"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        if self.calls == 1:
            return WorkerResult(False, error="external outcome unknown", retryable=False, side_effect_uncertain=True)
        return WorkerResult(True, {"ok": True})


class AlwaysUncertain(Worker):
    name = "always_uncertain"
    capabilities = {"research"}

    async def run(self, task):
        return WorkerResult(False, error="external outcome unknown", retryable=False, side_effect_uncertain=True)


class FixedPlanner:
    def plan(self, goal, context=None):
        return {"goal": goal, "steps": [{"capability": "research", "action": "research"}]}


def concurrent_unknown(db_path, mission_id):
    state = StateStore(db_path)
    runtime = type("Runtime", (), {"state": state})()
    try:
        return asyncio.run(reconcile_uncertain(runtime, mission_id, "unknown"))
    finally:
        state.conn.close()


async def run():
    with tempfile.NamedTemporaryFile(suffix=".db") as db:
        state = StateStore(db.name)
        workers = WorkerRegistry()
        worker = UncertainThenSuccess()
        workers.register(worker)
        runtime = JarvisRuntime(state=state, workers=workers, max_retries=2, retry_delay=0)
        runtime.planner = FixedPlanner()

        first = await runtime.submit("reconcile uncertain outcome")
        assert first["status"] == "failed"
        assert worker.calls == 1

        pending = json.loads(state.get_mission(first["mission_id"])["result"])
        assert pending["side_effect_uncertain"] is True
        assert pending["next_step"] == 0

        resumed = await reconcile_uncertain(runtime, first["mission_id"], "confirmed_not_applied")
        assert resumed["status"] == "completed"
        assert worker.calls == 2
        final = json.loads(state.get_mission(first["mission_id"])["result"])
        assert final["reconciliation"]["resolution"] == "confirmed_not_applied"
        assert "side_effect_uncertain" not in final

        applied_state = StateStore(db.name + ".applied")
        applied_workers = WorkerRegistry()
        applied_worker = UncertainThenSuccess()
        applied_workers.register(applied_worker)
        applied_runtime = JarvisRuntime(state=applied_state, workers=applied_workers, max_retries=2, retry_delay=0)
        applied_runtime.planner = FixedPlanner()
        applied = await applied_runtime.submit("confirmed external outcome")
        assert applied["status"] == "failed"
        assert applied_worker.calls == 1
        applied_result = await reconcile_uncertain(applied_runtime, applied["mission_id"], "confirmed_applied")
        assert applied_result["status"] == "completed"
        assert applied_worker.calls == 1
        applied_final = json.loads(applied_state.get_mission(applied["mission_id"])["result"])
        assert applied_final["next_step"] == 1
        assert applied_final["reconciliation"]["resolution"] == "confirmed_applied"
        assert "side_effect_uncertain" not in applied_final
        applied_state.conn.close()

        second_state = StateStore(db.name + ".second")
        second_workers = WorkerRegistry()
        second_workers.register(AlwaysUncertain())
        second_runtime = JarvisRuntime(state=second_state, workers=second_workers, max_retries=2, retry_delay=0)
        second_runtime.planner = FixedPlanner()
        second = await second_runtime.submit("unknown outcome remains unresolved")
        unresolved = await reconcile_uncertain(second_runtime, second["mission_id"], "unknown")
        assert unresolved["status"] == "failed"
        assert unresolved["reconciliation"] == "unknown"

        persisted_unknown = json.loads(second_state.get_mission(second["mission_id"])["result"])
        assert persisted_unknown["reconciliation"]["resolution"] == "unknown"
        event_count = second_state.conn.execute(
            "SELECT COUNT(*) FROM events WHERE mission_id=? AND kind='worker.uncertain_reconciled'",
            (second["mission_id"],),
        ).fetchone()[0]
        assert event_count == 1

        with ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(lambda _: concurrent_unknown(db.name + ".second", second["mission_id"]), range(3)))
        assert all(item["status"] == "failed" for item in results)
        assert all(item["reconciliation"] == "unknown" for item in results)
        event_count = second_state.conn.execute(
            "SELECT COUNT(*) FROM events WHERE mission_id=? AND kind='worker.uncertain_reconciled'",
            (second["mission_id"],),
        ).fetchone()[0]
        assert event_count == 1
        second_state.conn.close()


asyncio.run(run())
print("JARVIS-NEXT UNCERTAIN RECONCILIATION CONTRACT OK")
