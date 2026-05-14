from datetime import (
    datetime,
    timedelta
)


class DealPipeline:

    def __init__(self):

        pass

    def determine_stage(
        self,
        priority_action
    ):

        if (
            priority_action
            ==
            "priority_bid"
        ):

            return "proposal_ready"

        if (
            priority_action
            ==
            "recommended"
        ):

            return "review_queue"

        return "low_priority"

    def estimate_close_probability(
        self,
        score
    ):

        if score >= 100:

            return 80

        if score >= 70:

            return 60

        if score >= 40:

            return 40

        return 15

    def estimate_deal_value(
        self,
        budgets
    ):

        if not budgets:

            return "unknown"

        return budgets[0]

    def next_followup(
        self,
        probability
    ):

        if probability >= 70:

            days = 1

        elif probability >= 50:

            days = 3

        else:

            days = 7

        return (
            datetime.now()
            +
            timedelta(days=days)
        ).strftime(
            "%Y-%m-%d"
        )

    def process_project(
        self,
        item
    ):

        analysis = item.get(
            "project_analysis",
            {}
        )

        budgets = analysis.get(
            "budgets",
            []
        )

        score = item.get(
            "opportunity_score",
            0
        )

        priority_action = item.get(
            "priority_action",
            "low_priority"
        )

        stage = (
            self.determine_stage(
                priority_action
            )
        )

        probability = (
            self.estimate_close_probability(
                score
            )
        )

        deal_value = (
            self.estimate_deal_value(
                budgets
            )
        )

        followup = (
            self.next_followup(
                probability
            )
        )

        item[
            "deal_stage"
        ] = stage

        item[
            "close_probability"
        ] = probability

        item[
            "estimated_deal_value"
        ] = deal_value

        item[
            "next_followup"
        ] = followup

        return item

    def process(
        self,
        projects
    ):

        processed = []

        for item in projects:

            processed.append(
                self.process_project(
                    item
                )
            )

        processed.sort(
            key=lambda x: (
                x.get(
                    "close_probability",
                    0
                )
            ),
            reverse=True
        )

        return processed


deal_pipeline = (
    DealPipeline()
)