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


class EmailOutreachAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "EmailOutreachAgent"
        )

    async def execute(
        self,
        task
    ):

        queue = (
            approval_queue.load()
        )

        sent = []

        for item in queue:

            if (
                item.get(
                    "approval_status"
                )
                !=
                "approved"
            ):

                continue

            contact_email = (
                task.get(
                    "test_email"
                )
            )

            if not contact_email:

                continue

            result = (
                email_engine.send_project_proposal(
                    item,
                    contact_email
                )
            )

            if result.get(
                "success"
            ):

                telegram_engine.send_message(
                    f"EMAIL SENT:\n"
                    f"{contact_email}"
                )

                sent.append(
                    contact_email
                )

        return {

            "success": True,

            "sent":
                sent
        }