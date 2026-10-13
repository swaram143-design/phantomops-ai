import asyncio
import os
import tempfile

from .adapters import WorkerRegistry
from .permissions import PermissionEngine
from .phantomops_adapter import PhantomOpsAdapter
from .runtime import JarvisRuntime
from .state import StateStore


async def main():
    db = os.path.join(tempfile.gettempdir(), "jarvis_next_phantomops_revenue.db")
    try:
        os.remove(db)
    except FileNotFoundError:
        pass

    from agents.proposal_delivery_agent import ProposalDeliveryAgent

    original_send = ProposalDeliveryAgent.execute

    async def send(self, task):
        assert task["recipient"] == "owner@jarvis-test.example"
        assert task["proposal"]
        return {"success": True, "sent": True, "transport": "contract-test"}

    ProposalDeliveryAgent.execute = send

    try:
        registry = WorkerRegistry()
        registry.register(PhantomOpsAdapter())
        runtime = JarvisRuntime(
            StateStore(db),
            registry,
            PermissionEngine("WORK"),
            max_retries=0,
            retry_delay=0,
        )

        # Exercise the real PhantomOps worker and runtime approval flow while
        # keeping network-dependent lead discovery outside this deterministic test.
        runtime.planner.plan = lambda goal, context: {
            "goal": goal,
            "steps": [
                {"capability": "select_target", "action": "analyze"},
                {"capability": "proposal", "action": "draft"},
                {"capability": "crm_sync", "action": "workflow_trigger"},
                {"capability": "external_send", "action": "external_send"},
                {"capability": "followup_automation", "action": "workflow_trigger"},
            ],
            "source": "contract:phantomops_revenue",
        }

        context = {
            "leads": [{
                "company": "JARVIS Test Clinic",
                "email": "owner@jarvis-test.example",
                "need": "patient follow-up automation",
                "score": 9,
            }]
        }

        first = await runtime.submit("execute revenue workflow", context)
        assert first["status"] == "awaiting_approval", first
        assert first["step_index"] == 2, first
        assert first["context"]["company"] == "JARVIS Test Clinic", first
        assert first["context"]["pdf"].endswith("_proposal.pdf"), first

        crm = await runtime.resume(first["approval_id"], approved=True)
        assert crm["status"] == "awaiting_approval", crm
        assert crm["context"].get("crm_synced") is True, {
            "resume_result": crm,
            "mission_state": runtime.state.get_mission(first["mission_id"]),
        }
        assert crm["context"]["crm_id"].startswith("local-crm:"), crm

        sent = await runtime.resume(crm["approval_id"], approved=True)
        assert sent["status"] == "awaiting_approval", sent
        assert sent["context"]["sent"] is True, sent

        done = await runtime.resume(sent["approval_id"], approved=True)
        assert done["status"] == "completed", done
        assert done["context"]["followup_scheduled"] is True, done
        assert done["context"]["followup_email"] == "owner@jarvis-test.example", done

        crm_memory = __import__("tools.crm_memory", fromlist=["crm_memory"]).crm_memory
        assert crm_memory.find_contact("owner@jarvis-test.example") is not None

        followup_engine = __import__("tools.followup_engine", fromlist=["followup_engine"]).followup_engine
        assert any(item["email"] == "owner@jarvis-test.example" for item in followup_engine.load())

        print("JARVIS-NEXT REAL PHANTOMOPS REVENUE RUNTIME OK")
    finally:
        ProposalDeliveryAgent.execute = original_send


if __name__ == "__main__":
    asyncio.run(main())
