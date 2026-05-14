from agents.base_agent import (
    BaseAgent
)

from memory.approval_queue import (
    approval_queue
)

from tools.followup_engine import (
    followup_engine
)

from tools.telegram_engine import (
    telegram_engine
)


class FollowupAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "FollowupAgent"
        )

    async def execute(
        self,
        task
    ):

        queue = (
            approval_queue.load()
        )

        reminders = (
            followup_engine.process(
                queue
            )
        )

        for reminder in reminders:

            telegram_engine.send_message(
                reminder[
                    "message"
                ]
            )

        return {

            "success": True,

            "followups":
                reminders
        }