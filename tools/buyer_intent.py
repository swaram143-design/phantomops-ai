class BuyerIntent:

    def __init__(self):

        self.high_intent_keywords = [

            "need",
            "hiring",
            "looking for",
            "seeking",
            "developer needed",
            "automation expert",
            "consultant",
            "project",
            "freelance job",
            "contract",
            "workflow automation",
            "crm automation",
            "chatbot developer",
            "ai engineer"
        ]

        self.medium_intent_keywords = [

            "services",
            "solutions",
            "agency",
            "consulting",
            "automation company"
        ]

        self.low_value_keywords = [

            "best tools",
            "comparison",
            "guide",
            "tutorial",
            "review",
            "top 10",
            "how to",
            "blog",
            "vs",
            "examples",
            "tips"
        ]

        self.high_value_sources = [

            "upwork",
            "fiverr",
            "freelancer",
            "workana",
            "indeed",
            "linkedin",
            "glassdoor"
        ]

    def calculate_score(
        self,
        title,
        url
    ):

        score = 0

        title = title.lower()

        url = url.lower()

        for keyword in (
            self.high_intent_keywords
        ):

            if keyword in title:

                score += 30

        for keyword in (
            self.medium_intent_keywords
        ):

            if keyword in title:

                score += 10

        for keyword in (
            self.low_value_keywords
        ):

            if keyword in title:

                score -= 25

        for source in (
            self.high_value_sources
        ):

            if source in url:

                score += 25

        return score

    def classify(
        self,
        score
    ):

        if score >= 60:
            return "buyer_intent"

        if score >= 30:
            return "potential_interest"

        return "informational"

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

            score = (
                self.calculate_score(
                    title,
                    url
                )
            )

            classification = (
                self.classify(
                    score
                )
            )

            if (
                classification ==
                "informational"
            ):

                continue

            processed.append(
                {
                    "title": title,
                    "url": url,
                    "score": score,
                    "classification":
                        classification
                }
            )

        processed.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return processed


buyer_intent = BuyerIntent()