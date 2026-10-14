"""Legacy workflow compatibility surface routed through GOVI.

The historical workflow definitions are retained for compatibility, but this
module no longer activates the legacy in-process agent manager. GOVI owns
mission submission and JARVIS-NEXT owns execution, permissions, state, and
verification.
"""

import asyncio

from jarvis_next.govi_core import GoviCore


workflows = {
    "lead_generation": [
        ("scraper_agent", "Extract business leads"),
        ("research_agent", "Analyze lead quality"),
        ("outreach_agent", "Generate outreach campaign"),
        ("analytics_agent", "Generate workflow report"),
    ],
    "product_launch": [
        ("research_agent", "Analyze market demand"),
        ("product_agent", "Generate AI product"),
        ("outreach_agent", "Create marketing campaign"),
        ("analytics_agent", "Analyze launch performance"),
    ],
    "automation_execution": [
        ("automation_agent", "Execute automation workflow"),
        ("analytics_agent", "Track execution metrics"),
    ],
}

# Map historical labels to real JARVIS-NEXT worker capabilities/actions.
_CAPABILITY_MAP = {
    "scraper_agent": ("research", "research"),
    "research_agent": ("research", "research"),
    "outreach_agent": ("outreach_draft", "draft"),
    "analytics_agent": ("analytics", "analyze"),
    "product_agent": ("research", "draft"),
    "automation_agent": ("workflow_automation", "workflow_trigger"),
}


def run_workflow(workflow_name):
    """Submit each legacy workflow step to GOVI instead of executing locally."""
    if workflow_name not in workflows:
        print("Workflow not found.")
        return []

    govi = GoviCore()
    results = []
    for agent_name, task in workflows[workflow_name]:
        capability, action = _CAPABILITY_MAP[agent_name]
        goal = {
            "type": capability,
            "task": task,
            "legacy_workflow": workflow_name,
            "legacy_agent": agent_name,
            "step": {"capability": capability, "action": action},
        }
        results.append(asyncio.run(govi.submit(goal)))
    return results
