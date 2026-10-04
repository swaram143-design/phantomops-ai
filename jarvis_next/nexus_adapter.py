import asyncio
import importlib
import os
import sys
from .adapters import Worker, WorkerResult

class NexusLegacyAdapter(Worker):
    """
    Bridge JARVIS-NEXT to the stable NEXUS GRAM supervisor.

    JARVIS-NEXT owns mission state, permissions, approvals, retries and
    verification. GRAM remains the legacy organizational execution layer.
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
        self.supervisor = None

    def _load_supervisor(self):
        if self.supervisor is not None:
            return self.supervisor
        if not self.nexus_root:
            raise RuntimeError("NEXUS_ROOT is not configured")
        root = os.path.abspath(self.nexus_root)
        if root not in sys.path:
            sys.path.insert(0, root)
        module = importlib.import_module("gram.gram_supervisor")
        self.supervisor = getattr(module, "gram_supervisor", None)
        if self.supervisor is None:
            supervisor_cls = getattr(module, "GRAMSupervisor", None)
            if supervisor_cls is None:
                raise RuntimeError("NEXUS GRAMSupervisor not found")
            self.supervisor = supervisor_cls()
        return self.supervisor

    def score(self, task):
        if not self.nexus_root:
            return -100
        capability = task.get("step", {}).get("capability")
        return 80 if capability in self.capabilities else 0

    async def run(self, task):
        try:
            supervisor = self._load_supervisor()
            step = task.get("step", {})
            task_type = step.get("capability")
            if task_type not in supervisor.available_agents():
                return WorkerResult(False, error=f"NEXUS agent not available: {task_type}")

            payload = dict(task)
            payload["type"] = task_type
            result = await supervisor.execute(payload)
            if isinstance(result, dict):
                return WorkerResult(
                    bool(result.get("success", True)),
                    result,
                    result.get("error"),
                )
            return WorkerResult(True, result)
        except Exception as exc:
            return WorkerResult(False, error=str(exc), retryable=False)
