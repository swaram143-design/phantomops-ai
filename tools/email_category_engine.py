class EmailCategoryEngine:

    def __init__(self):

        self.categories = {

            "client_inquiry": {

                "keywords": {

                    "automation": 20,
                    "integration": 20,
                    "consultation": 25,
                    "proposal": 25,
                    "pricing": 25,
                    "project": 20,
                    "workflow": 20,
                    "meeting": 20,
                    "implementation": 20,
                    "service": 10,
                    "business": 10
                }
            },

            "recruiter": {

                "keywords": {

                    "job": 20,
                    "hiring": 25,
                    "position": 20,
                    "candidate": 20,
                    "resume": 20,
                    "interview": 25,
                    "recruiter": 30
                }
            },

            "financial_promo": {

                "keywords": {

                    "credit card": 40,
                    "loan": 40,
                    "platinum": 30,
                    "bank": 30,
                    "cashback": 35,
                    "emi": 35,
                    "finance": 30,
                    "card": 25
                }
            },

            "ecommerce": {

                "keywords": {

                    "shopping": 40,
                    "discount": 35,
                    "sale": 35,
                    "offer": 30,
                    "coupon": 40,
                    "deal": 25,
                    "cart": 30
                }
            },

            "newsletter": {

                "keywords": {

                    "newsletter": 40,
                    "weekly": 25,
                    "digest": 30,
                    "announcement": 20,
                    "update": 15
                }
            },

            "spam": {

                "keywords": {

                    "bitcoin": 50,
                    "crypto": 40,
                    "casino": 50,
                    "winner": 40,
                    "lottery": 50
                }
            }
        }

    def calculate_scores(
        self,
        combined
    ):

        scores = {}

        for category, config in (
            self.categories.items()
        ):

            score = 0

            keywords = (
                config.get(
                    "keywords",
                    {}
                )
            )

            for keyword, weight in (
                keywords.items()
            ):

                if keyword in combined:

                    score += weight

            scores[
                category
            ] = score

        return scores

    def classify(
        self,
        sender,
        subject,
        body
    ):

        combined = (
            (
                sender
                +
                " "
                +
                subject
                +
                " "
                +
                body
            ).lower()
        )

        scores = (
            self.calculate_scores(
                combined
            )
        )

        best_category = max(
            scores,
            key=scores.get
        )

        best_score = (
            scores[
                best_category
            ]
        )

        if best_score == 0:

            return {

                "category":
                    "unknown",

                "score":
                    0,

                "confidence":
                    "low"
            }

        confidence = "low"

        if best_score >= 80:

            confidence = "high"

        elif best_score >= 40:

            confidence = "medium"

        return {

            "category":
                best_category,

            "score":
                best_score,

            "confidence":
                confidence
        }


email_category_engine = (
    EmailCategoryEngine()
)