"""GOVI Core authority facade over the proven JARVIS-NEXT runtime.

GOVI is the executive authority in the NEXUS architecture.  The existing
JarvisRuntime remains the execution engine so the validated runtime contract
surface is preserved while callers migrate to GOVI terminology.
"""

from .bootstrap import build_registry
from .runtime import JarvisRuntime


class GoviCore:
    """Executive facade for mission submission, approval, and resumption."""

    def __init__(self, runtime=None, workers=None, **runtime_kwargs):
        if runtime is not None and workers is not None:
            raise ValueError("pass either runtime or workers, not both")
        self.runtime = runtime or JarvisRuntime(
            workers=workers if workers is not None else build_registry(),
            **runtime_kwargs,
        )

    async def submit(self, goal, context=None):
        return await self.runtime.submit(goal, context)

    async def resume_approval(self, approval_id, approved=True):
        return await self.runtime.resume(approval_id, approved)

    async def resume_mission(self, mission_id):
        return await self.runtime.resume_mission(mission_id)

    def mission_status(self, mission_id):
        return self.runtime.state.get_mission(mission_id)

    def health(self):
        return {
            "ok": True,
            "authority": "govi",
            "runtime": "jarvis_next",
            "runtime_type": type(self.runtime).__name__,
        }


GOVICore = GoviCore
