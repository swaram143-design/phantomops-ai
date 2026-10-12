from .planner import MissionPlanner


class InvalidModelRouter:
    def plan(self, goal, context):
        return {
            "steps": [
                {"capability": "research", "action": "external_send"}
            ]
        }


def main():
    planner = MissionPlanner(InvalidModelRouter())
    plan = planner.plan("find revenue opportunities")

    assert plan["source"] == "deterministic"
    assert plan["steps"][-1] == {
        "capability": "external_send",
        "action": "external_send",
    }
    assert all(
        not (
            step["capability"] == "research"
            and step["action"] == "external_send"
        )
        for step in plan["steps"]
    )

    print("JARVIS-NEXT PLANNER FALLBACK CONTRACT OK")


if __name__ == "__main__":
    main()
