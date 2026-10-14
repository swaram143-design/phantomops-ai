import asyncio

from .govi_core import GoviCore


class FakeState:
    def get_mission(self, mission_id):
        return {"id": mission_id, "status": "running"}


class FakeRuntime:
    def __init__(self):
        self.state = FakeState()
        self.calls = []

    async def submit(self, goal, context=None):
        self.calls.append(("submit", goal, context))
        return {"status": "accepted", "goal": goal, "context": context}

    async def resume(self, approval_id, approved=True):
        self.calls.append(("resume", approval_id, approved))
        return {"approval_id": approval_id, "approved": approved}

    async def resume_mission(self, mission_id):
        self.calls.append(("resume_mission", mission_id))
        return {"mission_id": mission_id, "status": "running"}


def main():
    runtime = FakeRuntime()
    govi = GoviCore(runtime=runtime)

    assert govi.health() == {
        "ok": True,
        "authority": "govi",
        "runtime": "jarvis_next",
        "runtime_type": "FakeRuntime",
    }
    assert asyncio.run(govi.submit("test goal", {"x": 1})) == {
        "status": "accepted",
        "goal": "test goal",
        "context": {"x": 1},
    }
    assert asyncio.run(govi.resume_approval("a1", False)) == {
        "approval_id": "a1",
        "approved": False,
    }
    assert asyncio.run(govi.resume_mission("m1")) == {
        "mission_id": "m1",
        "status": "running",
    }
    assert govi.mission_status("m1") == {"id": "m1", "status": "running"}
    assert runtime.calls == [
        ("submit", "test goal", {"x": 1}),
        ("resume", "a1", False),
        ("resume_mission", "m1"),
    ]
    print("GOVI CORE FACADE OK")


if __name__ == "__main__":
    main()
