class StrategicEngine:

    def __init__(self):

        self.priority_actions = {

            "buyer": {

                "high_priority_outreach":
                    {
                        "action":
                            "generate_personalized_outreach",
                        "urgency":
                            "high"
                    }
            },

            "provider": {

                "competitor_monitoring":
                    {
                        "action":
                            "track_services_and_pricing",
                        "urgency":
                            "medium"
                    }
            },

            "marketplace": {

                "mine_marketplace":
                    {
                        "action":
                            "extract_high_intent_projects",
                        "urgency":
                            "high"
                    }
            }
        }

    def determine_strategy(
        self,
        item
    ):

        direction = item.get(
            "commercial_direction",
            ""
        )

        action = item.get(
            "strategic_action",
            ""
        )

        strategy = (
            self.priority_actions
            .get(direction, {})
            .get(action, {})
        )

        return {

            "recommended_strategy":
                strategy.get(
                    "action",
                    "observe"
                ),

            "urgency":
                strategy.get(
                    "urgency",
                    "low"
                )
        }

    def process(
        self,
        opportunities
    ):

        processed = []

        for item in opportunities:

            strategy = (
                self.determine_strategy(
                    item
                )
            )

            item[
                "recommended_strategy"
            ] = strategy[
                "recommended_strategy"
            ]

            item[
                "execution_urgency"
            ] = strategy[
                "urgency"
            ]

            processed.append(
                item
            )

        processed.sort(
            key=lambda x: (
                100
                if x.get(
                    "execution_urgency"
                ) == "high"
                else 50
            ),
            reverse=True
        )

        return processed


strategic_engine = (
    StrategicEngine()
)