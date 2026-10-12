from .planner import MissionPlanner, PlanValidationError


def main():
    invalid_plans = [
        {"steps": [{"capability": "research", "action": "external_send"}]},
        {"steps": [{"capability": "research", "action": "external_call"}]},
        {"steps": [{"capability": "research", "action": "external_write"}]},
        {"steps": [{"capability": "research", "action": "workflow_trigger"}]},
    ]
    for plan in invalid_plans:
        try:
            MissionPlanner.validate("contract test", plan)
        except PlanValidationError:
            continue
        raise AssertionError(f"incompatible side-effect action accepted: {plan}")

    valid_plans = [
        {"steps": [{"capability": "external_send", "action": "external_send"}]},
        {"steps": [{"capability": "voice_receptionist", "action": "external_call"}]},
        {"steps": [{"capability": "crm_sync", "action": "external_write"}]},
        {"steps": [{"capability": "followup_automation", "action": "workflow_trigger"}]},
    ]
    for plan in valid_plans:
        MissionPlanner.validate("contract test", plan)

    print("JARVIS-NEXT PLANNER SIDE-EFFECT CONTRACT OK")


if __name__ == "__main__":
    main()
