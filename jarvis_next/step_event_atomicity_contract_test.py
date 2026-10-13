import tempfile

from .state import StateStore


def main():
    with tempfile.TemporaryDirectory() as tmp:
        store = StateStore(f"{tmp}/state.db")
        mid = store.create_mission("coupled step event test")
        owner = "owner-1"
        assert store.claim_mission(mid, owner, statuses=("queued",))
        before = store.get_mission(mid)
        original = store._insert_event

        def fail_step_event(kind, payload, mission_id=None):
            if kind == "step.completed":
                raise RuntimeError("step event write failed")
            return original(kind, payload, mission_id)

        store._insert_event = fail_step_event
        try:
            try:
                store.update_with_event(
                    mid,
                    lease_owner=owner,
                    status="running",
                    result={"next_step": 1},
                    event_kind="step.completed",
                    event_payload={"step_index": 0, "verified": True},
                )
            except RuntimeError as exc:
                assert str(exc) == "step event write failed"
            else:
                raise AssertionError("coupled update unexpectedly succeeded")
        finally:
            store._insert_event = original

        after = store.get_mission(mid)
        assert after["status"] == before["status"]
        assert after["result"] == before["result"]
        assert store.conn.execute("SELECT COUNT(*) FROM events WHERE mission_id=? AND kind='step.completed'", (mid,)).fetchone()[0] == 0
        assert store.conn.execute("SELECT COUNT(*) FROM events WHERE mission_id=? AND kind='mission.updated'", (mid,)).fetchone()[0] == 0
        print("step event atomicity contract passed")


if __name__ == "__main__":
    main()
