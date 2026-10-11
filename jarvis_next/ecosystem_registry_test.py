"""Contract test for the unified external ecosystem worker registry."""

from .bootstrap import build_registry
from .planner import MissionPlanner
from .permissions import PermissionEngine


def main():
    registry = build_registry()
    names = {worker.name for worker in registry.workers.values()}
    required = {"phantomops", "browser", "openclaw", "openhands", "ruflo", "paperclip", "ai_receptionist"}
    assert required.issubset(names), names

    plans = {
        "delegate this task to another company agent": "org_task",
        "run a multi agent swarm": "swarm",
        "build this software": "code",
        "find revenue opportunities": "research",
        "answer inbound phone calls as a receptionist": "voice_receptionist",
    }
    for goal, expected in plans.items():
        plan = MissionPlanner().plan(goal)
        assert plan["steps"], plan
        assert plan["steps"][0]["capability"] == expected, (goal, plan)

    assert registry.workers["ruflo"].score({"step": {"capability": "swarm"}}) > 0
    assert registry.workers["paperclip"].score({"step": {"capability": "org_task"}}) > 0
    assert registry.workers["ai_receptionist"].score({"step": {"capability": "voice_receptionist"}}) > 0

    # External calls must never become an unapproved safe action.
    decision = PermissionEngine("WORK").check("external_call")
    assert not decision.allowed and decision.requires_approval, decision

    health = registry.health()
    assert set(required).issubset(health), health
    print("JARVIS-NEXT ECOSYSTEM REGISTRY OK")


if __name__ == "__main__":
    main()
