from agents.base_agent import (
    BaseAgent
)

from tools.followup_engine import (
    followup_engine
)

from tools.email_tool import (
    email_tool
)

from tools.telegram_engine import (
    telegram_engine
)


class AutonomousFollowupAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "AutonomousFollowupAgent"
        )

    async def execute(
        self,
        task
    ):

        due_followups = (
            followup_engine.get_due_followups()
        )

        sent = []

        for item in due_followups:

            email = (
                item.get(
                    "email"
                )
            )

            company = (
                item.get(
                    "company"
                )
            )

            subject = (
                f"Following up regarding automation opportunities"
            )

            body = f"""
Hello {company},

I wanted to follow up regarding
our previous automation outreach.

We specialize in:
- AI automation
- workflow systems
- CRM integrations
- autonomous operations

Would you be available
for a quick discussion?

Best regards,
PhantomOps AI
"""

            result = (
                email_tool.send_email(
                    email,
                    subject,
                    body
                )
            )

            if result.get(
                "success"
            ):

                followup_engine.mark_sent(
                    email
                )

                telegram_engine.send_message(
                    f"FOLLOW-UP SENT\n\n"
                    f"{email}"
                )

                sent.append(
                    email
                )

        return {

            "success": True,

            "sent":
                sent
        }