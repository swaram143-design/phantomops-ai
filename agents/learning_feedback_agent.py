from agents.base_agent import (
    BaseAgent
)

from tools.learning_engine import (
    learning_engine
)

from tools.telegram_engine import (
    telegram_engine
)


class LearningFeedbackAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "LearningFeedbackAgent"
        )

    async def execute(
        self,
        task
    ):

        outcome = (
            task.get(
                "outcome"
            )
        )

        keywords = (
            task.get(
                "keywords",
                []
            )
        )

        if outcome == "win":

            learning_engine.record_win(
                keywords
            )

        elif outcome == "loss":

            learning_engine.record_loss(
                keywords
            )

        telegram_engine.send_message(
            f"LEARNING UPDATED\n\n"
            f"Outcome:\n"
            f"{outcome}\n\n"
            f"Keywords:\n"
            f"{keywords}"
        )

        return {

            "success": True,

            "learning":
                learning_engine.summary()
        }