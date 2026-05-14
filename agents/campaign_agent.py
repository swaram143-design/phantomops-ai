from agents.base_agent import (
    BaseAgent
)

from memory.approval_queue import (
    approval_queue
)

from tools.email_engine import (
    email_engine
)

from tools.telegram_engine import (
    telegram_engine
)

from tools.campaign_engine import (
    campaign_engine
)


class CampaignAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "CampaignAgent"
        )

    async def execute(
        self,
        task
    ):

        targets = (
            task.get(
                "targets",
                []
            )
        )

        campaign_name = (
            task.get(
                "campaign_name",
                "Campaign"
            )
        )

        queue = (
            approval_queue.load()
        )

        approved_projects = []

        for item in queue:

            if (
                item.get(
                    "approval_status"
                )
                ==
                "approved"
            ):

                approved_projects.append(
                    item
                )

        campaign_engine.create_campaign(
            campaign_name,
            targets
        )

        sent_count = 0

        for email in targets:

            for project in approved_projects:

                result = (
                    email_engine.send_project_proposal(
                        project,
                        email
                    )
                )

                if result.get(
                    "success"
                ):

                    sent_count += 1

                    campaign_engine.increment_sent(
                        campaign_name
                    )

                    telegram_engine.send_message(
                        f"CAMPAIGN EMAIL SENT\n"
                        f"{email}"
                    )

        return {

            "success": True,

            "campaign":
                campaign_name,

            "emails_sent":
                sent_count
        }