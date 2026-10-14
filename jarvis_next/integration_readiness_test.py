"""Contract tests for non-destructive integration readiness."""

from .integration_readiness import check_readiness


def test_readiness_does_not_claim_unconfigured_services_are_ready(monkeypatch):
    for key in (
        "JARVIS_N8N_WEBHOOK_URL",
        "JARVIS_N8N_WEBHOOK_TOKEN",
        "JARVIS_TWENTY_URL",
        "JARVIS_TWENTY_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)

    result = check_readiness()
    assert result["ready_for_controlled_revenue_mission"] is False
    assert result["integrations"]["n8n"] is False
    assert result["integrations"]["twenty"] is False
    assert result["integration_status"]["n8n"]["url_valid"] is False
    assert result["integration_status"]["twenty"]["url_valid"] is False
    assert result["side_effects_performed"] is False


def test_readiness_rejects_invalid_urls(monkeypatch):
    monkeypatch.setenv("JARVIS_N8N_WEBHOOK_URL", "not-a-url")
    monkeypatch.setenv("JARVIS_TWENTY_URL", "ftp://crm.example")
    monkeypatch.setenv("JARVIS_TWENTY_API_KEY", "test-only")

    result = check_readiness()
    assert result["ready_for_controlled_revenue_mission"] is False
    assert result["integrations"]["n8n"] is False
    assert result["integrations"]["twenty"] is False
    assert result["integration_status"]["n8n"]["url_valid"] is False
    assert result["integration_status"]["twenty"]["url_valid"] is False
    assert result["side_effects_performed"] is False


def test_readiness_preserves_approval_gates(monkeypatch):
    monkeypatch.setenv("JARVIS_N8N_WEBHOOK_URL", "https://example.invalid/webhook")
    monkeypatch.setenv("JARVIS_TWENTY_URL", "https://example.invalid")
    monkeypatch.setenv("JARVIS_TWENTY_API_KEY", "test-only")

    result = check_readiness()
    assert result["ready_for_controlled_revenue_mission"] is True
    assert result["integration_status"]["n8n"]["url_valid"] is True
    assert result["integration_status"]["twenty"]["url_valid"] is True
    for action in ("external_send", "external_call", "external_write", "workflow_trigger"):
        assert result["approval_gates"][action]["requires_approval"] is True
        assert result["approval_gates"][action]["allowed"] is False
    assert result["side_effects_performed"] is False
