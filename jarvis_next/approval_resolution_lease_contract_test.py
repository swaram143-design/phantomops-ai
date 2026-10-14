import os
import tempfile

from .state import StateStore


def _mission(state, status="awaiting_approval"):
    mid = state.create_mission("approved action")
    plan = {"steps": [{"action": "send_message", "capability": "email"}]}
    state.update(mid, status=status, plan=plan, result={"next_step": 0})
    aid = state.approval(mid, "send_message", {"step_index": 0, "step": plan["steps"][0], "context": {}, "results": [], "attempts": {}})
    return mid, aid, plan


def test_leased_approval_resolution_advances_mission():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        state = StateStore(path)
        mid, aid, _ = _mission(state)
        owner = "approval-owner"
        assert state.claim_mission(mid, owner, lease_seconds=5, statuses=("awaiting_approval",))
        resolved = state.resolve_approval(aid, "approved", lease_owner=owner)
        assert resolved and resolved["status"] == "approved"
        mission = state.get_mission(mid)
        assert mission["status"] == "running"
        assert mission["lease_owner"] == owner
        assert not state.pending_approval(mid)
    finally:
        try:
            state.conn.close()
        except Exception:
            pass
        os.remove(path)


def test_wrong_lease_owner_cannot_resolve_approval():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        state = StateStore(path)
        mid, aid, _ = _mission(state)
        owner = "approval-owner"
        assert state.claim_mission(mid, owner, lease_seconds=5, statuses=("awaiting_approval",))
        assert state.resolve_approval(aid, "approved", lease_owner="wrong-owner") is None
        approval = state.get_approval(aid)
        mission = state.get_mission(mid)
        assert approval["status"] == "pending"
        assert mission["status"] == "awaiting_approval"
        assert mission["lease_owner"] == owner
    finally:
        try:
            state.conn.close()
        except Exception:
            pass
        os.remove(path)


def test_expired_lease_does_not_resolve_or_orphan_approval():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        state = StateStore(path)
        mid, aid, _ = _mission(state)
        owner = "expired-owner"
        assert state.claim_mission(mid, owner, lease_seconds=0, statuses=("awaiting_approval",))
        assert state.resolve_approval(aid, "approved", lease_owner=owner) is None
        approval = state.get_approval(aid)
        mission = state.get_mission(mid)
        assert approval["status"] == "pending"
        assert mission["status"] == "awaiting_approval"
        assert state.pending_approval(mid)["id"] == aid
    finally:
        try:
            state.conn.close()
        except Exception:
            pass
        os.remove(path)


if __name__ == "__main__":
    test_leased_approval_resolution_advances_mission()
    test_wrong_lease_owner_cannot_resolve_approval()
    test_expired_lease_does_not_resolve_or_orphan_approval()
    print("approval resolution lease contract: PASS")
