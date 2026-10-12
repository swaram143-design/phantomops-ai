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

    # An invalid model plan must be rejected and replaced by the deterministic
    # planner. The deterministic planner currently resolves this goal through
    # the revenue prospecting recipe, which is still deterministic and does not
    # originate from the model router.
    assert plan["source"] == "recipe:revenue_prospecting"
    assert plan["steps"][-1] == {
        "capability": "followup_automation",
        "action": "workflow_trigger",
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
