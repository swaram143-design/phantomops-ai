class ContactIntelligence:

    def __init__(self):

        self.blocked_keywords = [

            ".png",
            ".jpg",
            ".jpeg",
            ".svg",
            "example",
            "your@email",
            "test@",
            "sample@",
            "demo@",
            "noreply",
            "no-reply"
        ]

        self.priority_keywords = [

            "founder",
            "ceo",
            "sales",
            "business",
            "contact",
            "hello",
            "info",
            "support"
        ]

    def is_valid_email(
        self,
        email
    ):

        email = email.lower()

        if "@" not in email:
            return False

        for keyword in (
            self.blocked_keywords
        ):

            if keyword in email:

                return False

        return True

    def calculate_score(
        self,
        email
    ):

        score = 0

        email = email.lower()

        for keyword in (
            self.priority_keywords
        ):

            if keyword in email:

                score += 10

        if email.endswith(".com"):
            score += 5

        return score

    def classify_contact(
        self,
        email
    ):

        score = self.calculate_score(
            email
        )

        if score >= 20:
            return "high_priority"

        if score >= 10:
            return "medium_priority"

        return "low_priority"

    def process_emails(
        self,
        emails
    ):

        processed = []

        unique_emails = list(
            set(emails)
        )

        for email in unique_emails:

            if not self.is_valid_email(
                email
            ):

                continue

            processed.append(
                {
                    "email": email,
                    "score":
                        self.calculate_score(
                            email
                        ),
                    "classification":
                        self.classify_contact(
                            email
                        )
                }
            )

        processed.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return processed


contact_intelligence = (
    ContactIntelligence()
)