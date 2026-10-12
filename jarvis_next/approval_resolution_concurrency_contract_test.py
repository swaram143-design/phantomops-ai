import tempfile
import threading

from .state import StateStore


def main():
    with tempfile.NamedTemporaryFile(suffix=".db") as db:
        first = StateStore(db.name)
        mission_id = first.create_mission("concurrent approval resolution")
        approval_id = first.approval(
            mission_id,
            "external_send",
            {"step_index": 0, "action": "external_send"},
        )
        first.conn.close()

        stores = [StateStore(db.name), StateStore(db.name)]
        barrier = threading.Barrier(2)
        results = []
        errors = []

        def resolve(store):
            try:
                barrier.wait()
                results.append(store.resolve_approval(approval_id, "approved"))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=resolve, args=(store,)) for store in stores]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert not errors, errors
        assert len(results) == 2
        claimed = [result for result in results if result is not None]
        skipped = [result for result in results if result is None]
        assert len(claimed) == 1, results
        assert len(skipped) == 1, results
        assert claimed[0]["status"] == "approved"
        assert stores[0].get_approval(approval_id)["status"] == "approved"

        for store in stores:
            store.conn.close()

    print("approval resolution concurrency contract: PASS")


if __name__ == "__main__":
    main()
