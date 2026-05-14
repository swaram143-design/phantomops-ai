from agents.base_agent import (
    BaseAgent
)

from tools.crm_sanitizer import (
    crm_sanitizer
)

from tools.telegram_engine import (
    telegram_engine
)


class CRMSanitizerAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "CRMSanitizerAgent"
        )

    async def execute(
        self,
        task
    ):

        result = (
            crm_sanitizer.sanitize()
        )

        telegram_engine.send_message(
            f"CRM SANITIZED\n\n"
            f"Removed:\n"
            f"{result.get('removed_count')}\n\n"
            f"Remaining:\n"
            f"{result.get('remaining_count')}"
        )

        return {

            "success": True,

            "result":
                result
        }