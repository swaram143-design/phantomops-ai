import imaplib
import email
import socket


socket.setdefaulttimeout(
    20
)


class InboxEngine:

    def __init__(self):

        self.email_address = (
            "phantomops.automation@gmail.com"
        )

        self.password = (
            "gvdt ngdp sbug kkjp"
        )

        self.low_value_keywords = [

            "unsubscribe",
            "coupon",
            "sale",
            "discount",
            "shopping",
            "deal",
            "offer"
        ]

        self.business_keywords = [

            "automation",
            "project",
            "integration",
            "meeting",
            "proposal",
            "consultation",
            "pricing",
            "service",
            "business",
            "schedule",
            "call",
            "implementation",
            "workflow"
        ]

    def connect(
        self
    ):

        mail = (
            imaplib.IMAP4_SSL(
                "imap.gmail.com"
            )
        )

        mail.login(
            self.email_address,
            self.password
        )

        return mail

    def score_email(
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

        score = 0

        if (
            "noreply"
            not in combined
        ):

            score += 20

        if (
            "no-reply"
            not in combined
        ):

            score += 20

        if (
            "@gmail.com"
            in sender.lower()
        ):

            score += 15

        for keyword in (
            self.business_keywords
        ):

            if keyword in combined:

                score += 15

        for keyword in (
            self.low_value_keywords
        ):

            if keyword in combined:

                score -= 20

        return score

    def fetch_unread_emails(
        self
    ):

        try:

            print(
                "[Inbox] Connecting..."
            )

            mail = self.connect()

            print(
                "[Inbox] Connected"
            )

            mail.select(
                "inbox"
            )

            print(
                "[Inbox] Searching unread emails..."
            )

            status, messages = (
                mail.search(
                    None,
                    "UNSEEN"
                )
            )

            email_ids = (
                messages[0]
                .split()
            )

            print(
                f"[Inbox] Found "
                f"{len(email_ids)} "
                f"unread emails"
            )

            collected = []

            for email_id in (
                email_ids[:25]
            ):

                status, data = (
                    mail.fetch(
                        email_id,
                        "(RFC822)"
                    )
                )

                raw_email = (
                    data[0][1]
                )

                msg = (
                    email.message_from_bytes(
                        raw_email
                    )
                )

                subject = (
                    msg.get(
                        "subject",
                        ""
                    )
                )

                sender = (
                    msg.get(
                        "from",
                        ""
                    )
                )

                body = ""

                if msg.is_multipart():

                    for part in msg.walk():

                        content_type = (
                            part.get_content_type()
                        )

                        if (
                            content_type
                            ==
                            "text/plain"
                        ):

                            payload = (
                                part.get_payload(
                                    decode=True
                                )
                            )

                            if payload:

                                body += (
                                    payload.decode(
                                        errors="ignore"
                                    )
                                )

                else:

                    payload = (
                        msg.get_payload(
                            decode=True
                        )
                    )

                    if payload:

                        body = (
                            payload.decode(
                                errors="ignore"
                            )
                        )

                email_score = (
                    self.score_email(
                        sender,
                        subject,
                        body
                    )
                )

                if (
                    email_score
                    <
                    25
                ):

                    continue

                collected.append(
                    {
                        "subject":
                            subject,

                        "sender":
                            sender,

                        "body":
                            body[:2000],

                        "score":
                            email_score
                    }
                )

            mail.logout()

            print(
                f"[Inbox] Processed "
                f"{len(collected)} "
                f"business emails"
            )

            return {

                "success": True,

                "emails":
                    collected
            }

        except Exception as error:

            return {

                "success": False,

                "error":
                    str(error)
            }

    def classify_email(
        self,
        email_data
    ):

        body = (
            email_data.get(
                "body",
                ""
            ).lower()
        )

        positive_keywords = [

            "interested",
            "meeting",
            "schedule",
            "call",
            "proposal",
            "next step",
            "available",
            "discuss",
            "pricing",
            "project",
            "automation",
            "integration",
            "consultation"
        ]

        for keyword in (
            positive_keywords
        ):

            if keyword in body:

                return "positive"

        return "neutral"


inbox_engine = (
    InboxEngine()
)