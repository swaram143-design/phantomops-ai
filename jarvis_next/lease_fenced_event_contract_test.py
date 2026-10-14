import tempfile

from .state import StateStore


def main():
    with tempfile.NamedTemporaryFile(suffix=".db") as db:
        state = StateStore(db.name)
        mid = state.create_mission("lease fenced event")
        state.update(mid, "running", plan={"steps": []}, result={})
        assert state.claim_mission(mid, "owner", lease_seconds=0.05, statuses=("running",))

        # Let the lease expire before attempting the standalone event write.
        import time
        time.sleep(0.08)
        assert state.event("worker.failed", {"stale": True}, mid, lease_owner="owner") is False

        events = state.conn.execute(
            "SELECT kind FROM events WHERE mission_id=? ORDER BY id", (mid,)
        ).fetchall()
        assert "worker.failed" not in [row["kind"] for row in events]
        assert state.get_mission(mid)["status"] == "running"

    print("JARVIS-NEXT LEASE-FENCED EVENT CONTRACT OK")


if __name__ == "__main__":
    main()
