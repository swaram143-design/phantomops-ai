from tools.crm_memory import (
    crm_memory
)


class CRMSanitizer:

    def __init__(self):

        self.blocked_patterns = [

            "no-reply",
            "noreply",
            "mailer-daemon",
            "googlemail",
            "accounts.google",
            "notification",
            "security alert"
        ]

    def sanitize(
        self
    ):

        contacts = (
            crm_memory.load()
        )

        cleaned = []

        removed = []

        for contact in contacts:

            email = (
                contact.get(
                    "email",
                    ""
                ).lower()
            )

            blocked = False

            for pattern in (
                self.blocked_patterns
            ):

                if pattern in email:

                    blocked = True

                    break

            if blocked:

                removed.append(
                    contact
                )

            else:

                cleaned.append(
                    contact
                )

        crm_memory.save(
            cleaned
        )

        return {

            "removed":
                removed,

            "remaining":
                cleaned,

            "removed_count":
                len(removed),

            "remaining_count":
                len(cleaned)
        }


crm_sanitizer = (
    CRMSanitizer()
)