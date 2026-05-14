from agents.base_agent import (
    BaseAgent
)

from tools.live_marketplace_scraper import (
    live_marketplace_scraper
)

from tools.marketplace_intelligence import (
    marketplace_intelligence
)

from tools.bid_generator import (
    bid_generator
)

from tools.approval_engine import (
    approval_engine
)

from tools.pipeline_engine import (
    pipeline_engine
)

from tools.telegram_engine import (
    telegram_engine
)


class LiveMarketplaceAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "LiveMarketplaceAgent"
        )

    async def execute(
        self,
        task
    ):

        projects = (
            live_marketplace_scraper.scrape_remoteok()
        )

        print(
            f"[Live Marketplace] "
            f"Found {len(projects)} projects"
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
                    ""
                )
            )

            print(
                f"[Project] {title}"
            )

            intelligence = (
                marketplace_intelligence.analyze_project(
                    title,
                    description
                )
            )

            print(
                f"[Score] "
                f"{intelligence.get('score')}"
            )

            if (

                intelligence.get(
                    "priority"
                )
                in [
                    "high",
                    "medium"
                ]

            ):

                bid = (
                    bid_generator.generate_bid(
                        title,
                        description
                    )
                )

                approval = (
                    approval_engine.add(
                        project,
                        bid,
                        intelligence.get(
                            "score"
                        )
                    )
                )

                pipeline_engine.create_opportunity(
                    client,
                    client
                )

                pipeline_engine.update_stage(
                    client,
                    "discovered",
                    title
                )

                telegram_engine.send_message(
                    f"LIVE PROJECT FOUND\n\n"
                    f"{title}\n\n"
                    f"Score:\n"
                    f"{intelligence.get('score')}"
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

                        "approval_id":
                            approval.get(
                                "id"
                            )
                    }
                )

        return {

            "success": True,

            "total_projects":
                len(projects),

            "processed":
                processed
        }