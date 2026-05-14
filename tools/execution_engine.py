class ExecutionEngine:

    def __init__(self):

        self.execution_map = {

            "high_priority_outreach":
                {
                    "execution":
                        "prepare_outreach_campaign",
                    "priority":
                        "critical"
                },

            "mine_marketplace":
                {
                    "execution":
                        "extract_projects_and_contacts",
                    "priority":
                        "high"
                },

            "competitor_monitoring":
                {
                    "execution":
                        "track_market_position",
                    "priority":
                        "medium"
                },

            "potential_partnership":
                {
                    "execution":
                        "prepare_partnership_analysis",
                    "priority":
                        "medium"
                }
        }

    def generate_execution_plan(
        self,
        item
    ):

        action = item.get(
            "strategic_action",
            ""
        )

        execution = (
            self.execution_map.get(
                action,
                {}
            )
        )

        return {

            "execution_task":
                execution.get(
                    "execution",
                    "observe"
                ),

            "execution_priority":
                execution.get(
                    "priority",
                    "low"
                )
        }

    def determine_next_step(
        self,
        execution_task
    ):

        next_steps = {

            "prepare_outreach_campaign":
                [
                    "extract_company_details",
                    "generate_personalized_message",
                    "queue_for_review"
                ],

            "extract_projects_and_contacts":
                [
                    "scrape_project_details",
                    "extract_client_requirements",
                    "identify_budget_signals"
                ],

            "track_market_position":
                [
                    "monitor_services",
                    "monitor_pricing",
                    "track_competitor_activity"
                ],

            "prepare_partnership_analysis":
                [
                    "analyze_platform",
                    "identify_integrations",
                    "evaluate_partnership_value"
                ]
        }

        return next_steps.get(
            execution_task,
            ["observe"]
        )

    def process(
        self,
        opportunities
    ):

        processed = []

        for item in opportunities:

            execution = (
                self.generate_execution_plan(
                    item
                )
            )

            execution_task = (
                execution[
                    "execution_task"
                ]
            )

            item[
                "execution_task"
            ] = execution_task

            item[
                "execution_priority"
            ] = execution[
                "execution_priority"
            ]

            item[
                "next_steps"
            ] = (
                self.determine_next_step(
                    execution_task
                )
            )

            processed.append(
                item
            )

        priority_order = {

            "critical": 100,

            "high": 75,

            "medium": 50,

            "low": 25
        }

        processed.sort(
            key=lambda x: (
                priority_order.get(
                    x.get(
                        "execution_priority",
                        "low"
                    ),
                    0
                )
            ),
            reverse=True
        )

        return processed


execution_engine = (
    ExecutionEngine()
)