import tempfile
import threading

from .state import StateStore


def run():
    with tempfile.TemporaryDirectory() as d:
        db = f"{d}/jarvis.db"
        first = StateStore(db)
        mid = first.create_mission("concurrent approval contract")
        first.update(mid, "awaiting_approval", plan={"steps": []}, result={"next_step": 0})
        first.conn.close()

        stores = [StateStore(db), StateStore(db)]
        barrier = threading.Barrier(2)
        ids = []
        errors = []

        def request(store):
            try:
                barrier.wait()
                ids.append(store.approval(mid, "send_email", {"step_index": 0, "action": "send_email"}))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=request, args=(store,)) for store in stores]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert not errors, errors
        assert len(ids) == 2
        assert ids[0] == ids[1], ids

        rows = stores[0].conn.execute(
            "SELECT COUNT(*) FROM approvals WHERE mission_id=? AND action=? AND status='pending'",
            (mid, "send_email"),
        ).fetchone()
        assert rows[0] == 1, rows[0]

        for store in stores:
            store.conn.close()

    print("approval concurrency contract: PASS")


if __name__ == "__main__":
    run()
