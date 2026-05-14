from agents.base_agent import (
    BaseAgent
)

from tools.browser_tools import (
    browser_tools
)

from tools.project_intelligence import (
    project_intelligence
)

from tools.proposal_engine import (
    proposal_engine
)

from tools.opportunity_scoring import (
    opportunity_scoring
)

from tools.deal_pipeline import (
    deal_pipeline
)

from tools.telegram_engine import (
    telegram_engine
)

from memory.memory_manager import (
    memory_manager
)

from memory.approval_queue import (
    approval_queue
)

from memory.client_memory import (
    client_memory
)


class MarketplaceMiningAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "MarketplaceMiningAgent"
        )

    async def execute(
        self,
        task
    ):

        marketplaces = [

            {
                "name":
                    "Upwork",

                "url":
                    "https://www.upwork.com/freelance-jobs/automation/"
            },

            {
                "name":
                    "PeoplePerHour",

                "url":
                    "https://www.peopleperhour.com/freelance-jobs"
            },

            {
                "name":
                    "Freelancer",

                "url":
                    "https://www.freelancer.com/jobs"
            }
        ]

        extracted_projects = []

        for marketplace in (
            marketplaces
        ):

            print(
                f"[MarketplaceMining] "
                f"Scanning: "
                f"{marketplace['name']}"
            )

            result = (
                await browser_tools.extract_page_content(
                    marketplace["url"]
                )
            )

            extracted_projects.append(
                {
                    "marketplace":
                        marketplace[
                            "name"
                        ],

                    "url":
                        marketplace[
                            "url"
                        ],

                    "content_preview":
                        result.get(
                            "content",
                            ""
                        )[:5000]
                }
            )

        analyzed = (
            project_intelligence.process(
                extracted_projects
            )
        )

        proposals = (
            proposal_engine.process(
                analyzed
            )
        )

        scored = (
            opportunity_scoring.process(
                proposals
            )
        )

        pipeline = (
            deal_pipeline.process(
                scored
            )
        )

        for item in pipeline:

            client_memory.remember_project(
                item
            )

            if (
                item.get(
                    "priority_action"
                )
                ==
                "priority_bid"
            ):

                telegram_engine.send_opportunity_alert(
                    item
                )

                approval_queue.add(
                    item
                )

        memory_manager.add_result(
            pipeline
        )

        memory_manager.add_event(
            {
                "agent": self.name,
                "action":
                    "client_memory_updated"
            }
        )

        return {
            "success": True,
            "projects":
                pipeline
        }