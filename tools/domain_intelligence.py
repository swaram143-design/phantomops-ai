from urllib.parse import (
    urlparse
)


class DomainIntelligence:

    def __init__(self):

        self.blocked_keywords = [

            "blog",
            "rank",
            "top",
            "best",
            "list",
            "directory",
            "review",
            "media",
            "news",
            "article",
            "compare",
            "vs",
            "guide"
        ]

        self.high_value_keywords = [

            "agency",
            "automation",
            "ai",
            "solutions",
            "studio",
            "labs",
            "systems",
            "digital",
            "software"
        ]

        self.blocked_domains = [

            "designrush",
            "influencermarketinghub",
            "themanifest",
            "guvi",
            "codeless",
            "medium",
            "reddit"
        ]

    def extract_domain(
        self,
        url
    ):

        try:

            parsed = urlparse(url)

            return parsed.netloc.lower()

        except:

            return ""

    def is_blocked_domain(
        self,
        domain
    ):

        for blocked in (
            self.blocked_domains
        ):

            if blocked in domain:

                return True

        return False

    def calculate_relevance(
        self,
        title,
        url
    ):

        score = 0

        title = title.lower()

        domain = self.extract_domain(
            url
        )

        if self.is_blocked_domain(
            domain
        ):

            return 0

        for keyword in (
            self.high_value_keywords
        ):

            if keyword in title:
                score += 15

            if keyword in domain:
                score += 10

        for keyword in (
            self.blocked_keywords
        ):

            if keyword in title:
                score -= 20

        if domain.endswith(".ai"):
            score += 20

        if domain.endswith(".io"):
            score += 10

        if domain.endswith(".com"):
            score += 5

        return score

    def classify_lead(
        self,
        score
    ):

        if score >= 40:
            return "high_value"

        if score >= 20:
            return "medium_value"

        return "low_value"

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
                self.calculate_relevance(
                    title,
                    url
                )
            )

            if score <= 0:
                continue

            processed.append(
                {
                    "title": title,
                    "url": url,
                    "score": score,
                    "classification":
                        self.classify_lead(
                            score
                        )
                }
            )

        processed.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return processed


domain_intelligence = (
    DomainIntelligence()
)