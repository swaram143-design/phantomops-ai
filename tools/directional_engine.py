class DirectionalEngine:

    def __init__(self):

        self.buyer_patterns = [

            "need",
            "looking for",
            "hiring",
            "seeking",
            "developer needed",
            "consultant needed",
            "job opening",
            "freelance project",
            "project available"
        ]

        self.provider_patterns = [

            "hire experts",
            "our services",
            "consulting services",
            "solutions",
            "agency",
            "we provide",
            "specialists",
            "experts",
            "automation company",
            "consultants"
        ]

        self.marketplace_patterns = [

            "freelance jobs",
            "work remote",
            "earn online",
            "projects in",
            "find jobs",
            "hire freelancers"
        ]

    def analyze_direction(
        self,
        title
    ):

        title = title.lower()

        buyer_score = 0
        provider_score = 0
        marketplace_score = 0

        for pattern in (
            self.buyer_patterns
        ):

            if pattern in title:

                buyer_score += 30

        for pattern in (
            self.provider_patterns
        ):

            if pattern in title:

                provider_score += 30

        for pattern in (
            self.marketplace_patterns
        ):

            if pattern in title:

                marketplace_score += 30

        scores = {

            "buyer":
                buyer_score,

            "provider":
                provider_score,

            "marketplace":
                marketplace_score
        }

        direction = max(
            scores,
            key=scores.get
        )

        return {
            "direction":
                direction,
            "scores":
                scores
        }

    def recommended_action(
        self,
        direction
    ):

        actions = {

            "buyer":
                "high_priority_outreach",

            "provider":
                "competitor_monitoring",

            "marketplace":
                "mine_marketplace"
        }

        return actions.get(
            direction,
            "observe"
        )

    def process(
        self,
        opportunities
    ):

        processed = []

        for item in opportunities:

            title = item.get(
                "title",
                ""
            )

            analysis = (
                self.analyze_direction(
                    title
                )
            )

            direction = (
                analysis[
                    "direction"
                ]
            )

            item[
                "commercial_direction"
            ] = direction

            item[
                "direction_scores"
            ] = analysis[
                "scores"
            ]

            item[
                "strategic_action"
            ] = (
                self.recommended_action(
                    direction
                )
            )

            processed.append(
                item
            )

        processed.sort(
            key=lambda x: (
                x.get(
                    "entity_score",
                    0
                )
                +
                x.get(
                    "score",
                    0
                )
            ),
            reverse=True
        )

        return processed


directional_engine = (
    DirectionalEngine()
)