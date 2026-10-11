"""Non-destructive readiness checks for JARVIS external integrations.

This module never sends a workflow, CRM write, message, call, or payment.
It only inspects local configuration and registered worker health metadata.
Use it before a controlled real revenue mission.
"""

from __future__ import annotations

import os
from typing import Any

from .bootstrap import build_registry
from .permissions import PermissionEngine


SENSITIVE_ACTIONS = ("external_send", "external_call", "external_write", "workflow_trigger")


def check_readiness() -> dict[str, Any]:
    registry = build_registry()
    health = registry.health()
    required = {
        "n8n": bool(os.getenv("JARVIS_N8N_WEBHOOK_URL")),
        "twenty": bool(
            os.getenv("JARVIS_TWENTY_URL") and os.getenv("JARVIS_TWENTY_API_KEY")
        ),
    }
    permission = PermissionEngine(os.getenv("JARVIS_PERMISSION", "WORK"))
    gates = {
        action: {
            "allowed": permission.check(action).allowed,
            "requires_approval": permission.check(action).requires_approval,
        }
        for action in SENSITIVE_ACTIONS
    }
    return {
        "ready_for_controlled_revenue_mission": all(required.values()),
        "integrations": required,
        "worker_health": health,
        "approval_gates": gates,
        "side_effects_performed": False,
    }


def format_readiness(result: dict[str, Any]) -> str:
    lines = ["JARVIS integration readiness", "-" * 28]
    for name, configured in result["integrations"].items():
        lines.append(f"{name}: {'configured' if configured else 'NOT configured'}")
    lines.append("Approval gates:")
    for action, gate in result["approval_gates"].items():
        lines.append(
            f"  {action}: approval_required={gate['requires_approval']}"
        )
    lines.append(
        "Controlled revenue mission: "
        + ("READY" if result["ready_for_controlled_revenue_mission"] else "NOT READY")
    )
    lines.append("Side effects performed: NO")
    return "\n".join(lines)


if __name__ == "__main__":
    result = check_readiness()
    print(format_readiness(result))
