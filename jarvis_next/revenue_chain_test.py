import asyncio
import os
import tempfile

from .adapters import Worker, WorkerRegistry, WorkerResult
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


class RevenueChainWorker(Worker):
    name = "revenue_chain_fake"
    capabilities = {"research", "opportunity", "select_target", "proposal", "external_send"}

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

        if capability == "external_send":
            assert context["company"] == "Acme Clinic"
            assert context["recipient"] == "owner@acme.example"
            assert context["proposal"]["total"] == 1500
            return WorkerResult(True, {"sent": True})

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

    # The approval pause must preserve every output produced before the send step.
    ctx = first["context"]
    assert ctx["research_marker"] == "research-complete", ctx
    assert ctx["opportunity_marker"] == "opportunity-complete", ctx
    assert ctx["company"] == "Acme Clinic", ctx
    assert ctx["recipient"] == "owner@acme.example", ctx
    assert ctx["selected_target"]["company"] == "Acme Clinic", ctx
    assert ctx["proposal"]["total"] == 1500, ctx
    assert set(ctx["step_outputs"]) == {"0", "1", "2", "3"}, ctx

    # Resume from the exact approval and prove the same context reaches delivery.
    done = await runtime.resume(first["approval_id"], approved=True)
    assert done["status"] == "completed", done
    assert done["context"]["company"] == "Acme Clinic", done
    assert done["context"]["recipient"] == "owner@acme.example", done
    assert done["context"]["proposal"]["total"] == 1500, done

    print("JARVIS-NEXT REVENUE CHAIN OK")


if __name__ == "__main__":
    asyncio.run(main())
