"""Non-destructive readiness checks for JARVIS external integrations.

This module never sends a workflow, CRM write, message, call, or payment.
It only inspects local configuration and registered worker health metadata.
Use it before a controlled real revenue mission.
"""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import urlparse

from .bootstrap import build_registry
from .permissions import PermissionEngine


SENSITIVE_ACTIONS = ("external_send", "external_call", "external_write", "workflow_trigger")


def _valid_http_url(value: str | None) -> bool:
    if not value or not value.strip():
        return False
    parsed = urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _integration_status(name: str, *, url: str | None, credential: str | None = None) -> dict[str, Any]:
    url_configured = _valid_http_url(url)
    credential_configured = credential is None or bool(credential.strip())
    return {
        "configured": url_configured and credential_configured,
        "url_valid": url_configured,
        "credential_present": credential is None or credential_configured,
        "non_destructive_probe_performed": False,
    }


def check_readiness() -> dict[str, Any]:
    registry = build_registry()
    health = registry.health()

    n8n_status = _integration_status(
        "n8n", url=os.getenv("JARVIS_N8N_WEBHOOK_URL"), credential=os.getenv("JARVIS_N8N_WEBHOOK_TOKEN")
    )
    twenty_status = _integration_status(
        "twenty", url=os.getenv("JARVIS_TWENTY_URL"), credential=os.getenv("JARVIS_TWENTY_API_KEY")
    )
    statuses = {"n8n": n8n_status, "twenty": twenty_status}
    required = {name: status["configured"] for name, status in statuses.items()}

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
        "integration_status": statuses,
        "worker_health": health,
        "approval_gates": gates,
        "side_effects_performed": False,
    }


def format_readiness(result: dict[str, Any]) -> str:
    lines = ["JARVIS integration readiness", "-" * 28]
    for name, configured in result["integrations"].items():
        status = result["integration_status"][name]
        lines.append(f"{name}: {'configured' if configured else 'NOT configured'}")
        lines.append(f"  url_valid={status['url_valid']} credential_present={status['credential_present']}")
    lines.append("Approval gates:")
    for action, gate in result["approval_gates"].items():
        lines.append(f"  {action}: approval_required={gate['requires_approval']}")
    lines.append(
        "Controlled revenue mission: "
        + ("READY" if result["ready_for_controlled_revenue_mission"] else "NOT READY")
    )
    lines.append("Side effects performed: NO")
    return "\n".join(lines)


if __name__ == "__main__":
    result = check_readiness()
    print(format_readiness(result))
