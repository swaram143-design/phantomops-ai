class SenderIntelligence:

    def __init__(self):

        self.blocked_patterns = [

            "no-reply",
            "noreply",
            "mailer-daemon",
            "notification",
            "notifications",
            "support@",
            "security alert",
            "accounts.google",
            "googlemail",
            "do-not-reply"
        ]

        self.high_value_patterns = [

            "ceo",
            "founder",
            "director",
            "manager",
            "operations",
            "business",
            "agency",
            "solutions",
            "technologies",
            "automation"
        ]

    def is_blocked(
        self,
        sender,
        subject=""
    ):

        combined = (
            (
                sender
                +
                " "
                +
                subject
            ).lower()
        )

        for pattern in (
            self.blocked_patterns
        ):

            if pattern in combined:

                return True

        return False

    def trust_score(
        self,
        sender
    ):

        sender = sender.lower()

        score = 50

        for pattern in (
            self.high_value_patterns
        ):

            if pattern in sender:

                score += 25

        if (
            "@gmail.com"
            in sender
        ):

            score += 10

        return score


sender_intelligence = (
    SenderIntelligence()
)