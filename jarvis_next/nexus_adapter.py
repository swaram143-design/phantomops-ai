import asyncio
import importlib
import os
import sys
from .adapters import Worker, WorkerResult

class NexusLegacyAdapter(Worker):
    """
    Bridge JARVIS-NEXT to the real NEXUS/GRAM TaskRouter.

    JARVIS-NEXT owns mission state, permissions and approvals. NEXUS/GRAM
    remains the legacy execution layer underneath it.
    """
    name = "nexus_legacy"
    capabilities = {
        "legacy_agent",
        "lead",
        "opportunity",
        "proposal",
        "proposal_delivery",
        "email_outreach",
        "followup",
        "analytics",
        "marketplace_mining",
        "marketplace_bidding",
        "live_marketplace",
        "outreach_draft",
        "campaign",
        "inbox_monitor",
        "autonomous_followup",
        "crm_sanitizer",
        "learning_feedback",
        "lead_intelligence",
        "executive_report",
        "govi",
    }

    def __init__(self, nexus_root=None):
        self.nexus_root = nexus_root or os.getenv("NEXUS_ROOT")
        self.router = None

    def _load_router(self):
        if self.router is not None:
            return self.router
        if not self.nexus_root:
            raise RuntimeError("NEXUS_ROOT is not configured")
        root = os.path.abspath(self.nexus_root)
        if root not in sys.path:
            sys.path.insert(0, root)
        module = importlib.import_module("gram.task_router")
        self.router = getattr(module, "task_router", None)
        if self.router is None:
            router_cls = getattr(module, "TaskRouter", None)
            if router_cls is None:
                raise RuntimeError("NEXUS GRAM TaskRouter not found")
            self.router = router_cls()
        return self.router

    def score(self, task):
        if not self.nexus_root:
            return -100
        capability = task.get("step", {}).get("capability")
        return 80 if capability in self.capabilities else 0

    async def run(self, task):
        try:
            router = self._load_router()
            step = task.get("step", {})
            task_type = step.get("capability")
            if task_type not in router.available_routes():
                return WorkerResult(False, error=f"NEXUS route not found: {task_type}")

            payload = dict(task)
            payload["type"] = task_type
            result = await router.route(payload)
            if isinstance(result, dict):
                return WorkerResult(
                    bool(result.get("success", True)),
                    result,
                    result.get("error"),
                )
            return WorkerResult(True, result)
        except Exception as exc:
            return WorkerResult(False, error=str(exc), retryable=False)
