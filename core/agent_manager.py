import time
import datetime

from core.logger import *

# =====================================================
# AGENTS
# =====================================================

agents = {

    "research_agent": {
        "role": "Market Research & Analysis",
        "status": "idle"
    },

    "scraper_agent": {
        "role": "Lead Extraction & Scraping",
        "status": "idle"
    },

    "outreach_agent": {
        "role": "Outreach & Campaigns",
        "status": "idle"
    },

    "automation_agent": {
        "role": "Workflow Automation",
        "status": "idle"
    },

    "product_agent": {
        "role": "AI Product Generation",
        "status": "idle"
    },

    "analytics_agent": {
        "role": "Performance Analytics",
        "status": "idle"
    }
}

# =====================================================
# SHOW AGENTS
# =====================================================

def show_agents():

    print("\n========== AGENT STATUS ==========\n")

    for name, info in agents.items():

        print(name)

        print(f"Role   : {info['role']}")

        print(f"Status : {info['status']}")

        print("--------------------------------")

# =====================================================
# ACTIVATE AGENT
# =====================================================

def activate_agent(agent_name, task):

    if agent_name not in agents:

        print("Agent not found.")

        return

    # =============================================
    # UPDATE STATUS
    # =============================================

    agents[agent_name]["status"] = "working"

    # =============================================
    # LOG START
    # =============================================

    write_log(
        f"{agent_name} started task: {task}"
    )

    # =============================================
    # DISPLAY
    # =============================================

    print("\n================================")

    print(f"AGENT ACTIVATED : {agent_name}")

    print(f"TASK            : {task}")

    print(
        f"TIME            : {datetime.datetime.now()}"
    )

    print("================================\n")

    print(f"{agent_name} executing...\n")

    time.sleep(1)

    # =============================================
    # COMPLETE
    # =============================================

    agents[agent_name]["status"] = "idle"

    write_log(
        f"{agent_name} completed task: {task}"
    )

    print(f"{agent_name} completed task.\n")