"""Reusable mission recipes built from registered workers.

Recipes describe orchestration only; workers keep the implementation. Authorization
is still enforced by PermissionEngine at runtime.
"""

RECIPES = {
    "revenue_prospecting": {
        "matches": ("revenue", "income", "find clients", "find leads", "prospects", "prospecting"),
        "steps": (
            ("research", "research"),
            ("opportunity", "analyze"),
            ("select_target", "analyze"),
            ("proposal", "draft"),
            # CRM creation/update is external state and therefore remains approval-gated.
            ("crm_sync", "workflow_trigger"),
            ("external_send", "external_send"),
            # Follow-up automation is also an external workflow and remains approval-gated.
            ("followup_automation", "workflow_trigger"),
        ),
    },
    "clinic_reactivation": {
        "matches": ("reactivate patients", "missed appointments", "follow up patients", "patient follow-up"),
        "steps": (("workflow_automation", "workflow_trigger"),),
    },
    "crm_sync": {
        "matches": ("sync crm", "sync lead to crm", "update crm", "crm workflow", "crm sync"),
        "steps": (("workflow_automation", "workflow_trigger"),),
    },
    "ai_receptionist": {
        "matches": ("ai receptionist", "answer inbound calls", "answer phone calls", "book appointments by phone"),
        "steps": (("voice_receptionist", "external_call"),),
    },
    "software_delivery": {
        "matches": ("build software", "build an app", "fix github", "develop software", "write code"),
        "steps": (("code", "local_code"), ("test", "test")),
    },
}


def resolve_recipe(goal):
    """Return the first matching recipe name and its orchestration steps."""
    text = (goal or "").strip().lower()
    for name, recipe in RECIPES.items():
        if any(term in text for term in recipe["matches"]):
            return name, recipe["steps"]
    return None, None


def build_recipe_plan(goal):
    """Build a validated-shape plan; planner validation remains authoritative."""
    name, steps = resolve_recipe(goal)
    if not steps:
        return None
    return {
        "goal": goal,
        "steps": [{"capability": capability, "action": action} for capability, action in steps],
        "source": f"recipe:{name}",
    }
