import asyncio
import json
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


class FakeWorker(Worker):
    def __init__(self, name, capability):
        self.name = name
        self.capabilities = {capability}
        self.calls = []

    async def run(self, task):
        self.calls.append(task)
        return WorkerResult(
            True,
            {
                "worker": self.name,
                "company": "Acme Clinic",
                "recipient": "owner@acme.example",
                "selected_target": "Acme Clinic",
                "selection_score": 91,
            },
        )


def test_revenue_chain_persists_and_resumes_across_approval_gates():
    async def scenario():
        with tempfile.TemporaryDirectory() as tmp:
            state = StateStore(f"{tmp}/jarvis.db")
            registry = WorkerRegistry()
            workers = {}
            for capability in (
                "research",
                "opportunity",
                "select_target",
                "proposal",
                "crm_sync",
                "external_send",
                "followup_automation",
            ):
                worker = FakeWorker(capability, capability)
                workers[capability] = worker
                registry.register(worker)

            runtime = JarvisRuntime(
                state=state,
                workers=registry,
                permissions=PermissionEngine("WORK"),
                max_retries=0,
            )
            plan = {
                "goal": "revenue mission",
                "steps": [
                    {"capability": "research", "action": "research"},
                    {"capability": "opportunity", "action": "analyze"},
                    {"capability": "select_target", "action": "analyze"},
                    {"capability": "proposal", "action": "draft"},
                    {"capability": "crm_sync", "action": "workflow_trigger"},
                    {"capability": "external_send", "action": "external_send"},
                    {"capability": "followup_automation", "action": "workflow_trigger"},
                ],
            }
            runtime.planner.plan = lambda goal, context: plan

            first = await runtime.submit("revenue mission")
            assert first["status"] == "awaiting_approval"
            assert first["step_index"] == 4
            crm_approval = first["approval_id"]

            persisted = state.get_mission(first["mission_id"])
            persisted_result = json.loads(persisted["result"])
            assert persisted["status"] == "awaiting_approval"
            assert persisted_result["next_step"] == 4
            assert persisted_result["context"]["company"] == "Acme Clinic"
            assert state.get_approval(crm_approval)["status"] == "pending"

            second = await runtime.resume(crm_approval, approved=True)
            assert second["status"] == "awaiting_approval"
            assert second["step_index"] == 5
            send_approval = second["approval_id"]
            assert state.get_approval(crm_approval)["status"] == "approved"

            third = await runtime.resume(send_approval, approved=True)
            assert third["status"] == "awaiting_approval"
            assert third["step_index"] == 6
            followup_approval = third["approval_id"]

            final = await runtime.resume(followup_approval, approved=True)
            assert final["status"] == "completed"
            assert len(final["results"]) == 7
            assert [w.calls[0]["step_index"] for w in workers.values()] == list(range(7))

            stored = state.get_mission(first["mission_id"])
            assert stored["status"] == "completed"
            stored_result = json.loads(stored["result"])
            assert stored_result["next_step"] == 7
            assert len(stored_result["results"]) == 7
            assert state.get_approval(send_approval)["status"] == "approved"
            assert state.get_approval(followup_approval)["status"] == "approved"

    asyncio.run(scenario())
