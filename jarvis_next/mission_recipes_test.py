from .mission_recipes import build_recipe_plan, resolve_recipe
from .planner import MissionPlanner


def main():
    name, steps = resolve_recipe("find clients for our AI automation service")
    assert name == "revenue_prospecting"
    assert [cap for cap, _ in steps] == [
        "research", "opportunity", "select_target", "proposal",
        "crm_sync", "external_send", "followup_automation",
    ]

    plan = build_recipe_plan("sync lead to CRM")
    assert plan["source"] == "recipe:crm_sync"
    assert plan["steps"] == [{"capability": "workflow_automation", "action": "workflow_trigger"}]

    planner = MissionPlanner()
    revenue = planner.plan("find clients for AI automation")
    assert revenue["source"] == "recipe:revenue_prospecting"
    assert [step["capability"] for step in revenue["steps"]] == [
        "research", "opportunity", "select_target", "proposal",
        "crm_sync", "external_send", "followup_automation",
    ]
    assert revenue["steps"][4]["action"] == "workflow_trigger"
    assert revenue["steps"][5]["action"] == "external_send"
    assert revenue["steps"][6]["action"] == "workflow_trigger"

    receptionist = planner.plan("build an AI receptionist to answer inbound calls")
    assert receptionist["source"] == "recipe:ai_receptionist"
    assert receptionist["steps"] == [{"capability": "voice_receptionist", "action": "external_call"}]

    software = planner.plan("build an app")
    assert software["source"] == "recipe:software_delivery"
    assert [step["capability"] for step in software["steps"]] == ["code", "test"]

    print("JARVIS-NEXT MISSION RECIPES OK")


if __name__ == "__main__":
    main()
