import tempfile

from .state import StateStore


def main():
    with tempfile.NamedTemporaryFile(suffix=".db") as db:
        first = StateStore(db.name)
        mid = first.create_mission("lease fencing")
        first.update(mid, "running", plan={"steps": []}, result={"next_step": 0})
        assert first.claim_mission(mid, "owner-1", lease_seconds=0.1, statuses=("running",))
        assert first.renew_mission(mid, "owner-1", lease_seconds=10)
        assert not first.claim_mission(mid, "owner-2", lease_seconds=10, statuses=("running",))

        second = StateStore(db.name)
        assert not second.claim_mission(mid, "owner-2", lease_seconds=10, statuses=("running",))
        assert first.release_mission(mid, "owner-1")
        assert second.claim_mission(mid, "owner-2", lease_seconds=10, statuses=("running",))

        try:
            first.update(mid, "completed", result={"next_step": 1}, lease_owner="owner-1")
        except RuntimeError as exc:
            assert str(exc) == "mission lease lost"
        else:
            raise AssertionError("stale lease owner must not update mission state")

    print("JARVIS-NEXT MISSION LEASE FENCING CONTRACT OK")


if __name__ == "__main__":
    main()
