"""Legacy JARVIS compatibility surface.

This historical module is retained so old imports do not become an accidental
second runtime. It deliberately contains no interactive loop, agent execution,
or independent task routing. Executive authority belongs to GOVI and execution
belongs to JARVIS-NEXT.
"""

from jarvis_next.govi_core import GoviCore


class LegacyJarvisFacade:
    """Explicit compatibility facade for callers migrating to GOVI."""

    def __init__(self, govi=None):
        self.govi = govi or GoviCore()

    async def submit(self, goal, context=None):
        return await self.govi.submit(goal, context)

    async def resume_approval(self, approval_id, approved=True):
        return await self.govi.resume_approval(approval_id, approved)

    async def resume_mission(self, mission_id):
        return await self.govi.resume_mission(mission_id)


# Compatibility name only. It is a facade over GOVI, not the old orchestrator.
Jarvis = LegacyJarvisFacade
jarvis = LegacyJarvisFacade()
