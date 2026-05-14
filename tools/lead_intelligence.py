class LeadIntelligence:

    def __init__(self):

        self.high_value_keywords = [

            "meeting",
            "consultation",
            "pricing",
            "proposal",
            "project",
            "automation",
            "integration",
            "workflow",
            "implementation",
            "service",
            "contract",
            "business",
            "schedule",
            "call",
            "discuss",
            "interested"
        ]

        self.low_value_keywords = [

            "unsubscribe",
            "coupon",
            "sale",
            "discount",
            "shopping",
            "android",
            "iphone",
            "deal",
            "offer"
        ]

        self.high_value_domains = [

            ".com",
            ".io",
            ".ai",
            ".tech",
            ".co"
        ]

    def score_sender(
        self,
        sender
    ):

        sender = sender.lower()

        score = 0

        if (
            "@gmail.com"
            in sender
        ):

            score += 20

        for domain in (
            self.high_value_domains
        ):

            if domain in sender:

                score += 10

        if (
            "noreply"
            not in sender
        ):

            score += 20

        if (
            "notification"
            not in sender
        ):

            score += 10

        return score

    def score_content(
        self,
        content
    ):

        content = content.lower()

        score = 0

        for keyword in (
            self.high_value_keywords
        ):

            if keyword in content:

                score += 15

        for keyword in (
            self.low_value_keywords
        ):

            if keyword in content:

                score -= 20

        return score

    def classify_priority(
        self,
        total_score
    ):

        if total_score >= 80:

            return "high_priority"

        if total_score >= 40:

            return "medium_priority"

        return "low_priority"

    def analyze_email(
        self,
        sender,
        subject,
        body
    ):

        sender_score = (
            self.score_sender(
                sender
            )
        )

        content_score = (
            self.score_content(
                subject
                +
                " "
                +
                body
            )
        )

        total_score = (
            sender_score
            +
            content_score
        )

        return {

            "sender_score":
                sender_score,

            "content_score":
                content_score,

            "total_score":
                total_score,

            "priority":
                self.classify_priority(
                    total_score
                )
        }


lead_intelligence = (
    LeadIntelligence()
)