from core.agent_manager import *

# =====================================================
# WORKFLOWS
# =====================================================

workflows = {

    "lead_generation": [

        (
            "scraper_agent",
            "Extract business leads"
        ),

        (
            "research_agent",
            "Analyze lead quality"
        ),

        (
            "outreach_agent",
            "Generate outreach campaign"
        ),

        (
            "analytics_agent",
            "Generate workflow report"
        )
    ],

    "product_launch": [

        (
            "research_agent",
            "Analyze market demand"
        ),

        (
            "product_agent",
            "Generate AI product"
        ),

        (
            "outreach_agent",
            "Create marketing campaign"
        ),

        (
            "analytics_agent",
            "Analyze launch performance"
        )
    ],

    "automation_execution": [

        (
            "automation_agent",
            "Execute automation workflow"
        ),

        (
            "analytics_agent",
            "Track execution metrics"
        )
    ]
}

# =====================================================
# RUN WORKFLOW
# =====================================================

def run_workflow(workflow_name):

    if workflow_name not in workflows:

        print("Workflow not found.")

        return

    print("\n================================")

    print(
        f"RUNNING WORKFLOW: {workflow_name}"
    )

    print("================================\n")

    workflow = workflows[workflow_name]

    # =============================================
    # EXECUTE TASKS
    # =============================================

    for agent_name, task in workflow:

        activate_agent(

            agent_name,

            task
        )

    # =============================================
    # COMPLETE
    # =============================================

    print("\n================================")

    print("WORKFLOW COMPLETED")

    print("================================\n")