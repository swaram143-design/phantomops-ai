import asyncio
import json
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor

from .adapters import Worker, WorkerRegistry, WorkerResult
from .runtime import JarvisRuntime
from .state import StateStore
from .uncertain_reconciliation import reconcile_uncertain


class AlwaysUncertain(Worker):
    name = "uncertain"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(False, error="external outcome unknown", retryable=False, side_effect_uncertain=True)


class SuccessWorker(Worker):
    name = "success"
    capabilities = {"research"}

    def __init__(self):
        self.calls = 0

    async def run(self, task):
        self.calls += 1
        return WorkerResult(True, data={"verified": True})


class FixedPlanner:
    def plan(self, goal, context):
        return {"steps": [{"action": "research", "capability": "research", "goal": goal}]}


def _transition(db_path, mission_id, expected_result, plan, result):
    state = StateStore(db_path)
    try:
        return state.reconcile_uncertain_transition(
            mission_id,
            expected_result,
            plan,
            result,
            {"resolution": "confirmed_not_applied", "previous_next_step": 0, "next_step": 0},
        )
    finally:
        state.conn.close()


async def run():
    db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db.close()
    try:
        initial_state = StateStore(db.name)
        uncertain = AlwaysUncertain()
        initial_workers = WorkerRegistry()
        initial_workers.register(uncertain)
        initial_runtime = JarvisRuntime(state=initial_state, workers=initial_workers, max_retries=2, retry_delay=0)
        initial_runtime.planner = FixedPlanner()
        failed = await initial_runtime.submit("concurrent uncertain reconciliation")
        assert failed["status"] == "failed"
        assert uncertain.calls == 1

        mission = initial_state.get_mission(failed["mission_id"])
        raw_result = mission["result"]
        plan = json.loads(mission["plan"])
        state = json.loads(raw_result)
        state["reconciliation"] = {"resolution": "confirmed_not_applied", "previous_next_step": 0}
        state["next_step"] = 0
        state.pop("side_effect_uncertain", None)

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(
                lambda _: _transition(db.name, failed["mission_id"], raw_result, plan, state),
                range(2),
            ))

        assert sorted(outcomes) == [False, True], outcomes
        claimed_mission = StateStore(db.name)
        try:
            persisted = claimed_mission.get_mission(failed["mission_id"])
            assert persisted["status"] == "running"
            persisted_result = json.loads(persisted["result"])
            assert persisted_result["reconciliation"]["resolution"] == "confirmed_not_applied"
            assert "side_effect_uncertain" not in persisted_result
        finally:
            claimed_mission.conn.close()

        restarted_state = StateStore(db.name)
        success = SuccessWorker()
        restarted_workers = WorkerRegistry()
        restarted_workers.register(success)
        restarted = JarvisRuntime(state=restarted_state, workers=restarted_workers, max_retries=2, retry_delay=0)
        restarted.planner = FixedPlanner()
        result = await restarted.resume_mission(failed["mission_id"])
        assert result["status"] == "completed"
        assert success.calls == 1
    finally:
        try:
            os.remove(db.name)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    asyncio.run(run())
