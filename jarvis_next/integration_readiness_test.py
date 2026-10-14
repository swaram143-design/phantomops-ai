"""Contract tests for non-destructive integration readiness."""

import os

from .integration_readiness import check_readiness


_KEYS = (
    "JARVIS_N8N_WEBHOOK_URL",
    "JARVIS_N8N_WEBHOOK_TOKEN",
    "JARVIS_TWENTY_URL",
    "JARVIS_TWENTY_API_KEY",
)


def _with_env(values):
    old = {key: os.environ.get(key) for key in _KEYS}
    try:
        for key in _KEYS:
            os.environ.pop(key, None)
        for key, value in values.items():
            os.environ[key] = value
        return check_readiness()
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def scenario():
    result = _with_env({})
    assert result["configured_for_controlled_revenue_mission"] is False
    assert result["ready_for_controlled_revenue_mission"] is False
    assert result["integrations"]["n8n"] is False
    assert result["integrations"]["twenty"] is False
    assert result["integration_status"]["n8n"]["url_valid"] is False
    assert result["integration_status"]["twenty"]["url_valid"] is False
    assert result["side_effects_performed"] is False

    result = _with_env({
        "JARVIS_N8N_WEBHOOK_URL": "not-a-url",
        "JARVIS_TWENTY_URL": "ftp://crm.example",
        "JARVIS_TWENTY_API_KEY": "test-only",
    })
    assert result["configured_for_controlled_revenue_mission"] is False
    assert result["ready_for_controlled_revenue_mission"] is False
    assert result["integrations"]["n8n"] is False
    assert result["integrations"]["twenty"] is False
    assert result["integration_status"]["n8n"]["url_valid"] is False
    assert result["integration_status"]["twenty"]["url_valid"] is False
    assert result["side_effects_performed"] is False

    result = _with_env({
        "JARVIS_N8N_WEBHOOK_URL": "https://example.invalid/webhook",
        "JARVIS_TWENTY_URL": "https://example.invalid",
        "JARVIS_TWENTY_API_KEY": "test-only",
    })
    assert result["configured_for_controlled_revenue_mission"] is True
    assert result["ready_for_controlled_revenue_mission"] is False
    assert result["readiness_basis"] == "configuration_only_no_network_probe"
    assert result["integration_status"]["n8n"]["url_valid"] is True
    assert result["integration_status"]["twenty"]["url_valid"] is True
    assert result["integration_status"]["n8n"]["non_destructive_probe_performed"] is False
    assert result["integration_status"]["twenty"]["non_destructive_probe_performed"] is False
    for action in ("external_send", "external_call", "external_write", "workflow_trigger"):
        assert result["approval_gates"][action]["requires_approval"] is True
        assert result["approval_gates"][action]["allowed"] is False
    assert result["side_effects_performed"] is False


def main():
    scenario()
    print("JARVIS-NEXT INTEGRATION READINESS CONTRACT OK")


if __name__ == "__main__":
    main()
