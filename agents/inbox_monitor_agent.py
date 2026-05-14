from agents.base_agent import (
    BaseAgent
)

from tools.inbox_engine import (
    inbox_engine
)

from tools.telegram_engine import (
    telegram_engine
)

from tools.campaign_engine import (
    campaign_engine
)

from tools.lead_intelligence import (
    lead_intelligence
)

from tools.email_category_engine import (
    email_category_engine
)

from tools.crm_memory import (
    crm_memory
)

from tools.pipeline_engine import (
    pipeline_engine
)

from tools.pipeline_intelligence import (
    pipeline_intelligence
)

from tools.sender_intelligence import (
    sender_intelligence
)


class InboxMonitorAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "InboxMonitorAgent"
        )

    async def execute(
        self,
        task
    ):

        result = (
            inbox_engine.fetch_unread_emails()
        )

        if not result.get(
            "success"
        ):

            return result

        emails = (
            result.get(
                "emails",
                []
            )
        )

        processed = []

        for email_data in emails:

            sender = (
                email_data.get(
                    "sender",
                    ""
                )
            )

            subject = (
                email_data.get(
                    "subject",
                    ""
                )
            )

            body = (
                email_data.get(
                    "body",
                    ""
                )
            )

            if (

                sender_intelligence.is_blocked(
                    sender,
                    subject
                )

            ):

                continue

            classification = (
                inbox_engine.classify_email(
                    email_data
                )
            )

            intelligence = (
                lead_intelligence.analyze_email(
                    sender,
                    subject,
                    body
                )
            )

            category = (
                email_category_engine.classify(
                    sender,
                    subject,
                    body
                )
            )

            trust_score = (
                sender_intelligence.trust_score(
                    sender
                )
            )

            crm_memory.create_contact(
                sender
            )

            crm_memory.add_interaction(
                sender,
                "email_received",
                subject
            )

            pipeline_engine.create_opportunity(
                sender,
                sender
            )

            detected_stage = (
                pipeline_intelligence.detect_stage(
                    subject,
                    body
                )
            )

            if detected_stage:

                pipeline_engine.update_stage(
                    sender,
                    detected_stage,
                    subject
                )

                telegram_engine.send_message(
                    f"PIPELINE STAGE UPDATED\n\n"
                    f"{sender}\n\n"
                    f"New Stage:\n"
                    f"{detected_stage}"
                )

            elif (

                category.get(
                    "category"
                )
                ==
                "client_inquiry"

            ):

                pipeline_engine.update_stage(
                    sender,
                    "engaged",
                    subject
                )

            processed.append(
                {
                    "sender":
                        sender,

                    "subject":
                        subject,

                    "classification":
                        classification,

                    "priority":
                        intelligence.get(
                            "priority"
                        ),

                    "score":
                        intelligence.get(
                            "total_score"
                        ),

                    "category":
                        category.get(
                            "category"
                        ),

                    "category_score":
                        category.get(
                            "score"
                        ),

                    "confidence":
                        category.get(
                            "confidence"
                        ),

                    "pipeline_stage":
                        detected_stage,

                    "trust_score":
                        trust_score
                }
            )

        return {

            "success": True,

            "processed":
                processed
        }