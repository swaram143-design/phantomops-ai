import asyncio
import importlib
import os
import sys
from .adapters import Worker, WorkerResult

class NexusLegacyAdapter(Worker):
    """
    Adapter around the existing local NEXUS/GRAM agent registry.

    JARVIS-NEXT remains the authority for mission state and permissions.
    This adapter only delegates an already-authorized step to legacy NEXUS
    workers. It is intentionally optional so PhantomOps can still run alone.
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
    }

    def __init__(self, nexus_root=None):
        self.nexus_root = nexus_root or os.getenv("NEXUS_ROOT")
        self.registry = None

    def _load_registry(self):
        if self.registry is not None:
            return self.registry
        if not self.nexus_root:
            raise RuntimeError("NEXUS_ROOT is not configured")
        root = os.path.abspath(self.nexus_root)
        if root not in sys.path:
            sys.path.insert(0, root)
        module = importlib.import_module("gram.agent_registry")
        self.registry = getattr(module, "agent_registry", None)
        if self.registry is None:
            registry_cls = getattr(module, "AgentRegistry", None)
            if registry_cls is None:
                raise RuntimeError("NEXUS GRAM AgentRegistry not found")
            self.registry = registry_cls()
        return self.registry

    def score(self, task):
        if not self.nexus_root:
            return -100
        step = task.get("step", {})
        capability = step.get("capability")
        if capability in self.capabilities:
            return 80
        return 0

    async def run(self, task):
        try:
            registry = self._load_registry()
            step = task.get("step", {})
            task_type = step.get("capability")
            agent = registry.get_agent(task_type)
            if agent is None:
                return WorkerResult(False, error=f"NEXUS agent not found: {task_type}")
            payload = dict(task)
            payload["type"] = task_type
            if hasattr(agent, "execute"):
                result = agent.execute(payload)
            elif hasattr(agent, "run"):
                result = agent.run(payload)
            else:
                return WorkerResult(False, error=f"NEXUS agent has no execute/run method: {task_type}")
            if asyncio.iscoroutine(result):
                result = await result
            if isinstance(result, dict):
                return WorkerResult(bool(result.get("success", True)), result, result.get("error"))
            return WorkerResult(True, result)
        except Exception as exc:
            return WorkerResult(False, error=str(exc), retryable=False)
