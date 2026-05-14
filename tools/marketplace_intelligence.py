from tools.learning_engine import (
    learning_engine
)


class MarketplaceIntelligence:

    def __init__(self):

        self.high_value_keywords = {

            "automation": 40,
            "ai": 40,
            "python": 35,
            "workflow": 30,
            "crm": 35,
            "agent": 35,
            "chatbot": 30,
            "lead generation": 35,
            "integration": 25,
            "saas": 30,
            "scraping": 25,
            "llm": 40,
            "openai": 40,
            "api": 20
        }

        self.blocked_keywords = [

            "marketing manager",
            "clinical",
            "nuclear",
            "seo",
            "population health",
            "attorney",
            "director",
            "quality manager",
            "sales manager",
            "operations associate"
        ]

    def analyze_project(
        self,
        title,
        description
    ):

        combined = (
            (
                title
                +
                " "
                +
                description
            ).lower()
        )

        for blocked in (
            self.blocked_keywords
        ):

            if blocked in combined:

                return {

                    "score": 0,

                    "priority":
                        "blocked",

                    "matched_keywords":
                        []
                }

        score = 0

        matched_keywords = []

        for keyword, weight in (
            self.high_value_keywords.items()
        ):

            if keyword in combined:

                adaptive_boost = (
                    learning_engine.keyword_boost(
                        keyword
                    )
                )

                final_weight = (
                    weight
                    +
                    adaptive_boost
                )

                score += final_weight

                matched_keywords.append(
                    keyword
                )

        priority = (
            "low"
        )

        if score >= 80:

            priority = (
                "high"
            )

        elif score >= 40:

            priority = (
                "medium"
            )

        return {

            "score":
                score,

            "priority":
                priority,

            "matched_keywords":
                matched_keywords
        }


marketplace_intelligence = (
    MarketplaceIntelligence()
)