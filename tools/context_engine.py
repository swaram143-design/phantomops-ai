class ContextEngine:

    def __init__(self):

        self.buyer_phrases = [

            "hiring",
            "looking for",
            "need help",
            "need developer",
            "seeking expert",
            "freelance project",
            "contract position",
            "consultant needed",
            "workflow specialist",
            "crm automation specialist"
        ]

        self.informational_phrases = [

            "top 10",
            "best tools",
            "guide",
            "tutorial",
            "how to",
            "tips",
            "examples",
            "ideas",
            "save hours",
            "blog",
            "comparison"
        ]

        self.marketplace_phrases = [

            "work remote",
            "earn online",
            "freelance jobs",
            "projects in",
            "hire freelancers"
        ]

        self.competitor_phrases = [

            "our services",
            "consulting",
            "solutions",
            "agency",
            "experts",
            "automation company"
        ]

    def detect_context(
        self,
        title
    ):

        title = title.lower()

        buyer_score = 0
        info_score = 0
        market_score = 0
        competitor_score = 0

        for phrase in (
            self.buyer_phrases
        ):

            if phrase in title:

                buyer_score += 25

        for phrase in (
            self.informational_phrases
        ):

            if phrase in title:

                info_score += 25

        for phrase in (
            self.marketplace_phrases
        ):

            if phrase in title:

                market_score += 25

        for phrase in (
            self.competitor_phrases
        ):

            if phrase in title:

                competitor_score += 20

        scores = {

            "buyer": buyer_score,

            "informational": info_score,

            "marketplace": market_score,

            "competitor": competitor_score
        }

        best_match = max(
            scores,
            key=scores.get
        )

        return {
            "classification":
                best_match,
            "scores":
                scores
        }

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
                self.detect_context(
                    title
                )
            )

            classification = (
                analysis[
                    "classification"
                ]
            )

            if (
                classification ==
                "informational"
            ):

                continue

            item[
                "semantic_classification"
            ] = classification

            item[
                "semantic_scores"
            ] = analysis[
                "scores"
            ]

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


context_engine = (
    ContextEngine()
)