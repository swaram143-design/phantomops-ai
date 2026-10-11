"""Contract test for the unified external ecosystem worker registry."""

from .bootstrap import build_registry
from .planner import MissionPlanner


def main():
    registry = build_registry()
    names = {worker.name for worker in registry.workers.values()}
    required = {"phantomops", "browser", "openclaw", "openhands", "ruflo", "paperclip"}
    assert required.issubset(names), names

    plans = {
        "delegate this task to another company agent": "org_task",
        "run a multi agent swarm": "swarm",
        "build this software": "code",
        "find revenue opportunities": "research",
    }
    for goal, expected in plans.items():
        plan = MissionPlanner().plan(goal)
        assert plan["steps"], plan
        assert plan["steps"][0]["capability"] == expected, (goal, plan)

    # Worker scoring must expose the external ecosystem without executing it.
    assert registry.find("ruflo").score({"step": {"capability": "swarm"}}) > 0
    assert registry.find("paperclip").score({"step": {"capability": "org_task"}}) > 0
    print("JARVIS-NEXT ECOSYSTEM REGISTRY OK")


if __name__ == "__main__":
    main()
