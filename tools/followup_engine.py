import json
import os

from datetime import (
    datetime,
    timedelta
)


FOLLOWUP_FILE = (
    "memory/followups.json"
)


class FollowupEngine:

    def __init__(self):

        self.ensure_memory()

    def ensure_memory(
        self
    ):

        if not os.path.exists(
            FOLLOWUP_FILE
        ):

            with open(
                FOLLOWUP_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

    def load(
        self
    ):

        try:

            with open(
                FOLLOWUP_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(
                    file
                )

                if isinstance(
                    data,
                    list
                ):

                    return data

                return []

        except:

            return []

    def save(
        self,
        data
    ):

        with open(
            FOLLOWUP_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def add_followup(
        self,
        email,
        company,
        days=2
    ):

        followups = (
            self.load()
        )

        followup = {

            "email":
                email,

            "company":
                company,

            "created_at":
                str(
                    datetime.now()
                ),

            "next_followup":
                str(
                    datetime.now()
                    +
                    timedelta(
                        days=days
                    )
                ),

            "status":
                "pending",

            "attempts":
                0
        }

        followups.append(
            followup
        )

        self.save(
            followups
        )

    def get_due_followups(
        self
    ):

        followups = (
            self.load()
        )

        due = []

        now = (
            datetime.now()
        )

        for item in followups:

            if (
                item.get(
                    "status"
                )
                !=
                "pending"
            ):

                continue

            followup_time = (
                datetime.fromisoformat(
                    item.get(
                        "next_followup"
                    )
                )
            )

            if (
                now
                >=
                followup_time
            ):

                due.append(
                    item
                )

        return due

    def mark_sent(
        self,
        email
    ):

        followups = (
            self.load()
        )

        for item in followups:

            if (
                item.get(
                    "email"
                )
                ==
                email
            ):

                item[
                    "attempts"
                ] += 1

                item[
                    "next_followup"
                ] = str(
                    datetime.now()
                    +
                    timedelta(
                        days=3
                    )
                )

                if (
                    item[
                        "attempts"
                    ]
                    >=
                    3
                ):

                    item[
                        "status"
                    ] = "closed"

        self.save(
            followups
        )


followup_engine = (
    FollowupEngine()
)