from agents.base_agent import (
    BaseAgent
)

from memory.contact_manager import (
    contact_manager
)

from memory.campaign_manager import (
    campaign_manager
)

from memory.memory_manager import (
    memory_manager
)

from memory.acquisition_memory import (
    acquisition_memory
)


class OutreachAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "OutreachAgent"
        )

    async def execute(self, task):

        contacts = (
            contact_manager.get_contacts()
        )

        generated_campaigns = []

        for contact in contacts:

            for email in contact[
                "emails"
            ]:

                if (
                    acquisition_memory.has_campaign(
                        email
                    )
                ):

                    continue

                acquisition_memory.add_campaign(
                    email
                )

                message = f"""
Hello,

I came across {contact['company']}
and noticed your company may
benefit from AI automation systems.

We specialize in:
- AI operators
- workflow automation
- lead generation
- intelligent business systems
- operational AI infrastructure

Would you be interested in a
quick discussion?

Best regards,
PhantomOps AI
"""

                campaign_manager.create_campaign(
                    contact[
                        "company"
                    ],
                    email,
                    message
                )

                generated_campaigns.append(
                    {
                        "company":
                            contact[
                                "company"
                            ],

                        "email":
                            email,

                        "status":
                            "pending_review"
                    }
                )

        memory_manager.add_event(
            {
                "agent": self.name,
                "action":
                    "deduplicated_campaigns_generated"
            }
        )

        return {
            "success": True,
            "campaigns":
                generated_campaigns
        }