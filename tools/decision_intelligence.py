class DecisionIntelligence:

    def __init__(self):

        self.high_priority = [

            "founder",
            "ceo",
            "owner",
            "partner",
            "partnership",
            "sales",
            "business",
            "growth",
            "hello"
        ]

        self.medium_priority = [

            "info",
            "contact",
            "support"
        ]

        self.low_priority = [

            "career",
            "jobs",
            "hr",
            "recruit",
            "admin"
        ]

        self.rejected_keywords = [

            ".png",
            ".jpg",
            ".jpeg",
            "noreply",
            "no-reply",
            "example",
            "your@email"
        ]

        self.region_aliases = [

            "london",
            "poland",
            "romania",
            "bulgaria",
            "spain",
            "norway",
            "amsterdam",
            "lisbon",
            "latam",
            "portugal",
            "new.york",
            "chicago"
        ]

    def reject_email(
        self,
        email
    ):

        email = email.lower()

        for keyword in (
            self.rejected_keywords
        ):

            if keyword in email:

                return True

        for alias in (
            self.region_aliases
        ):

            if alias in email:

                return True

        return False

    def calculate_priority(
        self,
        email
    ):

        email = email.lower()

        score = 0

        for keyword in (
            self.high_priority
        ):

            if keyword in email:

                score += 30

        for keyword in (
            self.medium_priority
        ):

            if keyword in email:

                score += 15

        for keyword in (
            self.low_priority
        ):

            if keyword in email:

                score -= 10

        if email.endswith(".com"):
            score += 5

        return score

    def classify_priority(
        self,
        score
    ):

        if score >= 40:
            return "executive"

        if score >= 20:
            return "business"

        return "low"

    def process_contacts(
        self,
        contacts
    ):

        processed = []

        seen = set()

        for contact in contacts:

            email = contact.get(
                "email",
                ""
            )

            if not email:
                continue

            if email in seen:
                continue

            seen.add(email)

            if self.reject_email(
                email
            ):

                continue

            score = (
                self.calculate_priority(
                    email
                )
            )

            classification = (
                self.classify_priority(
                    score
                )
            )

            processed.append(
                {
                    "email": email,
                    "score": score,
                    "priority":
                        classification
                }
            )

        processed.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return processed


decision_intelligence = (
    DecisionIntelligence()
)