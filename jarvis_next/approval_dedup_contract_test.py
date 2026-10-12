import tempfile

from .state import StateStore


def main():
    with tempfile.NamedTemporaryFile(suffix=".db") as db:
        state = StateStore(db.name)
        mission_id = state.create_mission("send the approved message")
        payload = {
            "step_index": 0,
            "step": {"capability": "external_send", "action": "external_send"},
            "context": {"recipient": "test@example.invalid"},
            "results": [],
            "attempts": {},
        }

        first = state.approval(mission_id, "external_send", payload)
        second = state.approval(mission_id, "external_send", payload)

        assert first == second, "identical pending approvals must be reused"
        rows = state.conn.execute(
            "SELECT COUNT(*) AS count FROM approvals WHERE mission_id=?",
            (mission_id,),
        ).fetchone()
        assert rows["count"] == 1

        different = dict(payload)
        different["step_index"] = 1
        third = state.approval(mission_id, "external_send", different)
        assert third != first, "different approval payloads must remain distinct"

    print("JARVIS-NEXT APPROVAL DEDUP CONTRACT OK")


if __name__ == "__main__":
    main()
