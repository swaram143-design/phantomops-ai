class OpportunityIntelligence:

    def __init__(self):

        self.high_intent_keywords = [

            "need",
            "looking for",
            "hiring",
            "seeking",
            "automation",
            "ai engineer",
            "workflow",
            "crm",
            "chatbot",
            "lead generation",
            "outreach",
            "integrations",
            "ai developer",
            "business automation"
        ]

        self.high_value_sources = [

            "reddit",
            "upwork",
            "fiverr",
            "linkedin",
            "wellfound",
            "hackernews",
            "github"
        ]

    def calculate_intent(
        self,
        title,
        source
    ):

        score = 0

        title = title.lower()

        source = source.lower()

        for keyword in (
            self.high_intent_keywords
        ):

            if keyword in title:

                score += 15

        for platform in (
            self.high_value_sources
        ):

            if platform in source:

                score += 20

        return score

    def classify_opportunity(
        self,
        score
    ):

        if score >= 50:
            return "high_intent"

        if score >= 25:
            return "medium_intent"

        return "low_intent"

    def process_results(
        self,
        results
    ):

        processed = []

        for result in results:

            title = result.get(
                "title",
                ""
            )

            url = result.get(
                "url",
                ""
            )

            score = (
                self.calculate_intent(
                    title,
                    url
                )
            )

            processed.append(
                {
                    "title": title,
                    "url": url,
                    "score": score,
                    "classification":
                        self.classify_opportunity(
                            score
                        )
                }
            )

        processed.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return processed


opportunity_intelligence = (
    OpportunityIntelligence()
)