from agents.marketing_agent import marketing_agent

from agents.marketplace_mining_agent import (
    MarketplaceMiningAgent
)

from agents.marketplace_bidding_agent import (
    MarketplaceBiddingAgent
)

from agents.live_marketplace_agent import (
    LiveMarketplaceAgent
)

from agents.followup_agent import (
    FollowupAgent
)

from agents.outreach_draft_agent import (
    OutreachDraftAgent
)

from agents.email_outreach_agent import (
    EmailOutreachAgent
)

from agents.campaign_agent import (
    CampaignAgent
)

from agents.inbox_monitor_agent import (
    InboxMonitorAgent
)

from agents.autonomous_followup_agent import (
    AutonomousFollowupAgent
)

from agents.proposal_agent import (
    ProposalAgent
)

from agents.proposal_delivery_agent import (
    ProposalDeliveryAgent
)

from agents.learning_feedback_agent import (
    LearningFeedbackAgent
)

from agents.analytics_agent import (
    AnalyticsAgent
)

from agents.crm_sanitizer_agent import (
    CRMSanitizerAgent
)


class Jarvis:

    def __init__(self):

        self.agents = {

            "marketplace_mining":
                MarketplaceMiningAgent(),

            "marketplace_bidding":
                MarketplaceBiddingAgent(),

            "live_marketplace":
                LiveMarketplaceAgent(),

            "followup":
                FollowupAgent(),

            "draft_outreach":
                OutreachDraftAgent(),

            "email_outreach":
                EmailOutreachAgent(),

            "campaign":
                CampaignAgent(),

            "inbox_monitor":
                InboxMonitorAgent(),

            "autonomous_followup":
                AutonomousFollowupAgent(),

            "proposal":
                ProposalAgent(),

            "proposal_delivery":
                ProposalDeliveryAgent(),

            "learning_feedback":
                LearningFeedbackAgent(),

            "analytics":
                AnalyticsAgent(),

            "crm_sanitizer":
                CRMSanitizerAgent()
        }

    async def execute(
        self,
        task, elif task["type"] == "marketing":

    return {

        "success": True,

        "instagram_post":
            marketing_agent.generate_instagram_post(),

        "whatsapp_pitch":
            marketing_agent.generate_whatsapp_pitch(),

        "cold_email":
            marketing_agent.generate_cold_email(),

        "offer":
            marketing_agent.generate_offer(),

        "landing_page":
            marketing_agent.generate_landing_page_text()
    }
    ):

        task_type = (
            task.get(
                "type"
            )
        )

        agent = (
            self.agents.get(
                task_type
            )
        )

        if not agent:

            return {

                "success": False,

                "error":
                    f"No agent found for {task_type}"
            }

        try:

            result = await agent.execute(
                task
            )

            return result

        except Exception as error:

            return {

                "success": False,

                "error":
                    str(error)
            }

    async def execute_goal(
        self,
        goal
    ):

        return await self.execute(
            goal
        )


jarvis = (
    Jarvis()
)