import asyncio
import os
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


class RevenueChainWorker(Worker):
    name = "revenue_chain_fake"
    capabilities = {
        "research", "opportunity", "select_target", "proposal",
        "crm_sync", "external_send", "followup_automation",
    }

    async def run(self, task):
        capability = task["step"]["capability"]
        context = task["context"]

        if capability == "research":
            return WorkerResult(True, {
                "leads": [{"company": "Acme Clinic", "email": "owner@acme.example"}],
                "research_marker": "research-complete",
            })

        if capability == "opportunity":
            assert context["leads"][0]["company"] == "Acme Clinic"
            return WorkerResult(True, {
                "opportunities": [{"company": "Acme Clinic", "email": "owner@acme.example",
                                   "need": "patient follow-up automation", "score": 9}],
                "opportunity_marker": "opportunity-complete",
            })

        if capability == "select_target":
            assert context["opportunities"][0]["need"] == "patient follow-up automation"
            return WorkerResult(True, {
                "company": "Acme Clinic",
                "need": "patient follow-up automation",
                "recipient": "owner@acme.example",
                "selected_target": context["opportunities"][0],
                "selection_score": 15,
            })

        if capability == "proposal":
            assert context["company"] == "Acme Clinic"
            assert context["recipient"] == "owner@acme.example"
            return WorkerResult(True, {
                "proposal": {"company": "Acme Clinic", "total": 1500},
                "proposal_marker": "proposal-complete",
            })

        if capability == "crm_sync":
            assert context["company"] == "Acme Clinic"
            assert context["recipient"] == "owner@acme.example"
            assert context["proposal"]["total"] == 1500
            return WorkerResult(True, {
                "crm_synced": True,
                "crm_marker": "crm-sync-complete",
                "crm_id": "crm-acme-001",
            })

        if capability == "external_send":
            assert context["company"] == "Acme Clinic"
            assert context["recipient"] == "owner@acme.example"
            assert context["proposal"]["total"] == 1500
            assert context["crm_synced"] is True
            return WorkerResult(True, {"sent": True, "send_marker": "send-complete"})

        if capability == "followup_automation":
            assert context["company"] == "Acme Clinic"
            assert context["crm_id"] == "crm-acme-001"
            assert context["sent"] is True
            return WorkerResult(True, {
                "followup_scheduled": True,
                "followup_marker": "followup-complete",
            })

        return WorkerResult(False, error=f"unexpected capability: {capability}")


async def main():
    db = os.path.join(tempfile.gettempdir(), "jarvis_next_revenue_chain.db")
    try:
        os.remove(db)
    except FileNotFoundError:
        pass

    registry = WorkerRegistry()
    registry.register(RevenueChainWorker())

    runtime = JarvisRuntime(
        StateStore(db),
        registry,
        PermissionEngine("WORK"),
        max_retries=0,
        retry_delay=0,
    )

    first = await runtime.submit("find revenue opportunities")
    assert first["status"] == "awaiting_approval", first
    assert first["step_index"] == 4, first
    assert set(first["context"]["step_outputs"]) == {"0", "1", "2", "3"}, first

    # Approval 1: CRM sync. No CRM side effect is executed before approval.
    crm_approval = first["approval_id"]
    crm = await runtime.resume(crm_approval, approved=True)
    assert crm["status"] == "awaiting_approval", crm
    assert crm["step_index"] == 5, crm
    assert crm["context"]["crm_marker"] == "crm-sync-complete", crm
    assert crm["context"]["crm_id"] == "crm-acme-001", crm

    # Approval 2: external proposal delivery. The approved send executes,
    # then JARVIS pauses before the next external follow-up workflow.
    send = await runtime.resume(crm["approval_id"], approved=True)
    assert send["status"] == "awaiting_approval", send
    assert send["step_index"] == 6, send
    assert send["context"]["sent"] is True, send
    assert send["context"]["crm_id"] == "crm-acme-001", send

    # Approval 3: follow-up workflow.
    done = await runtime.resume(send["approval_id"], approved=True)
    assert done["status"] == "completed", done
    assert done["context"]["company"] == "Acme Clinic", done
    assert done["context"]["recipient"] == "owner@acme.example", done
    assert done["context"]["proposal"]["total"] == 1500, done
    assert done["context"]["crm_synced"] is True, done
    assert done["context"]["sent"] is True, done
    assert done["context"]["followup_scheduled"] is True, done

    print("JARVIS-NEXT REVENUE CHAIN OK")


if __name__ == "__main__":
    asyncio.run(main())
