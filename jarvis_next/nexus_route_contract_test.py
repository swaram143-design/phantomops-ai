from .nexus_adapter import NexusLegacyAdapter


# Source-derived from the stable NEXUS GRAM task_router route table.
EXPECTED_NEXUS_ROUTES = {
    "lead",
    "opportunity",
    "marketplace_mining",
    "marketplace_bidding",
    "live_marketplace",
    "proposal",
    "proposal_delivery",
    "email_outreach",
    "followup",
    "autonomous_followup",
    "outreach_draft",
    "campaign",
    "analytics",
    "learning_feedback",
    "crm_sanitizer",
    "inbox_monitor",
    "lead_intelligence",
    "executive_report",
    "govi",
}


def main():
    adapter = NexusLegacyAdapter("/configured/nexus")
    missing = EXPECTED_NEXUS_ROUTES - adapter.capabilities
    assert not missing, f"JARVIS adapter missing NEXUS routes: {sorted(missing)}"
    print("JARVIS-NEXT NEXUS ROUTE CONTRACT OK")


if __name__ == "__main__":
    main()
