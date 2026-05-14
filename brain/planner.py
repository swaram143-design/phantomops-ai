class Planner:

    def __init__(self):

        self.task_map = {

            "lead_generation": [
                "LeadScraperAgent"
            ],

            "outreach": [
                "OutreachAgent"
            ],

            "opportunity_discovery": [
                "OpportunityAgent"
            ],

            "marketplace_mining": [
                "MarketplaceMiningAgent"
            ],

            "draft_outreach": [
                "OutreachDraftAgent"
            ]
        }

    async def create_plan(
        self,
        goal
    ):

        goal_type = goal.get(
            "type"
        )

        plan = {

            "goal": goal,

            "agents": [],

            "steps": []
        }

        if goal_type in (
            self.task_map
        ):

            assigned_agents = (
                self.task_map[
                    goal_type
                ]
            )

            plan["agents"] = (
                assigned_agents
            )

            for agent in (
                assigned_agents
            ):

                plan[
                    "steps"
                ].append(
                    {
                        "agent":
                            agent,

                        "status":
                            "pending"
                    }
                )

        return plan


planner = Planner()