from tools.learning_engine import (
    learning_engine
)

from tools.pipeline_engine import (
    pipeline_engine
)

from tools.crm_memory import (
    crm_memory
)


class AnalyticsEngine:

    def revenue_summary(
        self
    ):

        pipeline = (
            pipeline_engine.summary()
        )

        learning = (
            learning_engine.summary()
        )

        contacts = (
            crm_memory.top_leads()
        )

        wins = sum(

            learning.get(
                "wins",
                {}
            ).values()
        )

        losses = sum(

            learning.get(
                "losses",
                {}
            ).values()
        )

        total = (
            wins
            +
            losses
        )

        win_rate = 0

        if total > 0:

            win_rate = round(

                (
                    wins
                    /
                    total
                )
                * 100,
                2
            )

        return {

            "pipeline":
                pipeline,

            "wins":
                wins,

            "losses":
                losses,

            "win_rate":
                win_rate,

            "top_keywords":
                learning.get(
                    "wins",
                    {}
                ),

            "top_contacts":
                contacts
        }


analytics_engine = (
    AnalyticsEngine()
)