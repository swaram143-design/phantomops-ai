from agents.base_agent import (
    BaseAgent
)

from tools.marketplace_intelligence import (
    marketplace_intelligence
)

from tools.bid_generator import (
    bid_generator
)

from tools.telegram_engine import (
    telegram_engine
)

from tools.pipeline_engine import (
    pipeline_engine
)

from tools.approval_engine import (
    approval_engine
)


class MarketplaceBiddingAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "MarketplaceBiddingAgent"
        )

    async def execute(
        self,
        task
    ):

        projects = (
            task.get(
                "projects",
                []
            )
        )

        processed = []

        for project in projects:

            title = (
                project.get(
                    "title",
                    ""
                )
            )

            description = (
                project.get(
                    "description",
                    ""
                )
            )

            client = (
                project.get(
                    "client",
                    "Unknown"
                )
            )

            intelligence = (
                marketplace_intelligence.analyze_project(
                    title,
                    description
                )
            )

            if (

                intelligence.get(
                    "priority"
                )
                ==
                "high"

            ):

                bid = (
                    bid_generator.generate_bid(
                        title,
                        description
                    )
                )

                pipeline_engine.create_opportunity(
                    client,
                    client
                )

                pipeline_engine.update_stage(
                    client,
                    "contacted",
                    title
                )

                approval_item = (
                    approval_engine.add(
                        project,
                        bid,
                        intelligence.get(
                            "score"
                        )
                    )
                )

                telegram_engine.send_message(
                    f"APPROVAL REQUIRED\n\n"
                    f"{title}\n\n"
                    f"Approval ID:\n"
                    f"{approval_item.get('id')}"
                )

                processed.append(
                    {
                        "title":
                            title,

                        "client":
                            client,

                        "score":
                            intelligence.get(
                                "score"
                            ),

                        "priority":
                            intelligence.get(
                                "priority"
                            ),

                        "approval_id":
                            approval_item.get(
                                "id"
                            ),

                        "bid":
                            bid
                    }
                )

        return {

            "success": True,

            "processed":
                processed
        }