import tempfile

from .state import StateStore


def main():
    with tempfile.NamedTemporaryFile(suffix=".db") as db:
        state = StateStore(db.name)
        mission_id = state.create_mission("send the approved message")
        plan = {
            "goal": "send the approved message",
            "steps": [{"capability": "external_send", "action": "external_send"}],
        }
        state.update(mission_id, status="awaiting_approval", plan=plan, result={"next_step": 0})
        approval_id = state.approval(
            mission_id,
            "external_send",
            {
                "step_index": 0,
                "step": plan["steps"][0],
                "context": {},
                "results": [],
                "attempts": {},
            },
        )

        tampered_plan = {
            "goal": plan["goal"],
            "steps": [{"capability": "external_call", "action": "external_call"}],
        }
        state.update(mission_id, status="awaiting_approval", plan=tampered_plan, result={"next_step": 0})

        try:
            state.resolve_approval(approval_id, "approved")
        except ValueError as exc:
            assert str(exc) == "Approval no longer matches the stored mission plan"
        else:
            raise AssertionError("approval must not resolve against a changed mission plan")

        assert state.get_approval(approval_id)["status"] == "pending"

    print("JARVIS-NEXT APPROVAL PLAN BINDING OK")


if __name__ == "__main__":
    main()
