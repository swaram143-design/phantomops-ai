import tempfile

from .state import StateStore


def main():
    with tempfile.TemporaryDirectory() as tmp:
        store = StateStore(f"{tmp}/state.db")
        mid = store.create_mission("atomic event test")
        before = store.get_mission(mid)
        original = store._insert_event

        def fail_event(*args, **kwargs):
            raise RuntimeError("event write failed")

        store._insert_event = fail_event
        try:
            try:
                store.update(mid, status="running", result={"next_step": 1})
            except RuntimeError as exc:
                assert str(exc) == "event write failed"
            else:
                raise AssertionError("update unexpectedly succeeded")
        finally:
            store._insert_event = original

        after = store.get_mission(mid)
        assert after["status"] == before["status"]
        assert after["result"] == before["result"]
        assert store.conn.execute("SELECT COUNT(*) FROM events WHERE mission_id=? AND kind='mission.updated'", (mid,)).fetchone()[0] == 0

        store.update(mid, status="running", result={"next_step": 1})
        after_success = store.get_mission(mid)
        assert after_success["status"] == "running"
        assert store.conn.execute("SELECT COUNT(*) FROM events WHERE mission_id=? AND kind='mission.updated'", (mid,)).fetchone()[0] == 1
        print("state event atomicity contract passed")


if __name__ == "__main__":
    main()
