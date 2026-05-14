class EntityIntelligence:

    def __init__(self):

        self.marketplaces = [

            "upwork",
            "fiverr",
            "freelancer",
            "peopleperhour",
            "workana",
            "truelancer"
        ]

        self.buyers = [

            "hiring",
            "need",
            "looking for",
            "seeking",
            "job",
            "project",
            "consultant",
            "developer"
        ]

        self.competitors = [

            "agency",
            "services",
            "solutions",
            "consulting",
            "experts",
            "hire workflow"
        ]

        self.informational = [

            "blog",
            "guide",
            "top",
            "best",
            "review",
            "comparison",
            "tutorial",
            "how to"
        ]

    def classify(
        self,
        title,
        url
    ):

        title = title.lower()

        url = url.lower()

        for keyword in (
            self.informational
        ):

            if keyword in title:

                return "informational"

        for source in (
            self.marketplaces
        ):

            if source in url:

                return "marketplace"

        for keyword in (
            self.buyers
        ):

            if keyword in title:

                return "buyer"

        for keyword in (
            self.competitors
        ):

            if keyword in title:

                return "competitor"

        return "unknown"

    def score_entity(
        self,
        entity_type
    ):

        scores = {

            "buyer": 100,

            "marketplace": 80,

            "competitor": 40,

            "informational": 0,

            "unknown": 10
        }

        return scores.get(
            entity_type,
            0
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

            url = item.get(
                "url",
                ""
            )

            entity_type = (
                self.classify(
                    title,
                    url
                )
            )

            if (
                entity_type ==
                "informational"
            ):

                continue

            processed.append(
                {
                    "title": title,
                    "url": url,
                    "entity_type":
                        entity_type,
                    "entity_score":
                        self.score_entity(
                            entity_type
                        ),
                    "score":
                        item.get(
                            "score",
                            0
                        )
                }
            )

        processed.sort(
            key=lambda x: (
                x["entity_score"]
                + x["score"]
            ),
            reverse=True
        )

        return processed


entity_intelligence = (
    EntityIntelligence()
)