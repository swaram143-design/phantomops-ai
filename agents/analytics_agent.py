from agents.base_agent import (
    BaseAgent
)

from tools.analytics_engine import (
    analytics_engine
)

from tools.telegram_engine import (
    telegram_engine
)


class AnalyticsAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "AnalyticsAgent"
        )

    async def execute(
        self,
        task
    ):

        summary = (
            analytics_engine.revenue_summary()
        )

        telegram_engine.send_message(
            f"ANALYTICS UPDATED\n\n"
            f"Win Rate:\n"
            f"{summary.get('win_rate')}%"
        )

        return {

            "success": True,

            "analytics":
                summary
        }