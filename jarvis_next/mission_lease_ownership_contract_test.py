import tempfile
from .state import StateStore


def main():
    with tempfile.NamedTemporaryFile(suffix=".db") as db:
        state = StateStore(db.name)
        mid = state.create_mission("lease ownership")
        state.update(mid, "running", plan={"steps": []}, result={"next_step": 0})
        assert state.claim_mission(mid, "owner-1", lease_seconds=10, statuses=("running",))
        assert state.has_mission_lease(mid, "owner-1")
        assert not state.has_mission_lease(mid, "owner-2")
        assert state.release_mission(mid, "owner-1")
        assert not state.has_mission_lease(mid, "owner-1")

    print("JARVIS-NEXT MISSION LEASE OWNERSHIP CONTRACT OK")


if __name__ == "__main__":
    main()
