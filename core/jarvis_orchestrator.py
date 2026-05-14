import json
import os
import datetime

# =====================================================
# MEMORY FILE
# =====================================================

MEMORY_FILE = "memory/system_memory.json"

# =====================================================
# CREATE MEMORY
# =====================================================

def initialize_memory():

    if not os.path.exists("memory"):

        os.makedirs("memory")

    if not os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "w") as file:

            json.dump([], file)

# =====================================================
# SAVE MEMORY
# =====================================================

def save_memory(event):

    with open(MEMORY_FILE, "r") as file:

        data = json.load(file)

    timestamp = str(
        datetime.datetime.now()
    )

    data.append({

        "timestamp": timestamp,
        "event": event
    })

    with open(MEMORY_FILE, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )

# =====================================================
# LOAD MEMORY
# =====================================================

def load_memory():

    with open(MEMORY_FILE, "r") as file:

        return json.load(file)

# =====================================================
# AGENT REGISTRY
# =====================================================

agents = {

    "jobs_agent": "Zero2Earn AI Job System",

    "research_agent": "Research & Analysis System",

    "automation_agent": "Workflow Automation Engine",

    "product_agent": "Nexora Product Creator",

    "outreach_agent": "PhantomOps Outreach System",

    "recruiter_agent": "Recruitment Pipeline System"
}

# =====================================================
# WORKFLOW ROUTER
# =====================================================

def route_task(task):

    task = task.lower()

    # =================================================
    # JOBS WORKFLOW
    # =================================================

    if (
        "job" in task
        or "income" in task
        or "freelance" in task
    ):

        save_memory(
            f"Jobs Agent Activated: {task}"
        )

        return (
            "Routing task to Jobs Agent..."
        )

    # =================================================
    # RESEARCH WORKFLOW
    # =================================================

    elif (
        "research" in task
        or "analyze" in task
        or "study" in task
    ):

        save_memory(
            f"Research Agent Activated: {task}"
        )

        return (
            "Routing task to Research Agent..."
        )

    # =================================================
    # PRODUCT WORKFLOW
    # =================================================

    elif (
        "product" in task
        or "ebook" in task
        or "pdf" in task
    ):

        save_memory(
            f"Product Agent Activated: {task}"
        )

        return (
            "Routing task to Product Agent..."
        )

    # =================================================
    # OUTREACH WORKFLOW
    # =================================================

    elif (
        "lead" in task
        or "client" in task
        or "outreach" in task
    ):

        save_memory(
            f"Outreach Agent Activated: {task}"
        )

        return (
            "Routing task to Outreach Agent..."
        )

    # =================================================
    # AUTOMATION WORKFLOW
    # =================================================

    elif (
        "automation" in task
        or "workflow" in task
        or "execute" in task
    ):

        save_memory(
            f"Automation Agent Activated: {task}"
        )

        return (
            "Routing task to Automation Agent..."
        )

    # =================================================
    # DEFAULT
    # =================================================

    else:

        save_memory(
            f"Unknown Task: {task}"
        )

        return (
            "Task recognized but no workflow assigned."
        )

# =====================================================
# START SYSTEM
# =====================================================

initialize_memory()

print("\n================================")
print("     JARVIS ORCHESTRATOR")
print("================================")

print("\nAI Operating Core Online.\n")

# =====================================================
# MAIN LOOP
# =====================================================

while True:

    task = input(
        "\nJARVIS COMMAND > "
    )

    if task.lower() == "exit":

        print(
            "\nShutting down orchestrator..."
        )

        break

    response = route_task(task)

    print(f"\n{response}")