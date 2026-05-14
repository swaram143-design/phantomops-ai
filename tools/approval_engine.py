import json
import os

from datetime import (
    datetime
)


APPROVAL_FILE = (
    "memory/approval_queue.json"
)


class ApprovalEngine:

    def __init__(self):

        self.ensure_memory()

    def ensure_memory(
        self
    ):

        if not os.path.exists(
            APPROVAL_FILE
        ):

            with open(
                APPROVAL_FILE,
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
                APPROVAL_FILE,
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
            APPROVAL_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def add(
        self,
        project,
        bid,
        score
    ):

        approvals = (
            self.load()
        )

        item = {

            "id":
                len(
                    approvals
                ) + 1,

            "project":
                project,

            "bid":
                bid,

            "score":
                score,

            "status":
                "pending",

            "created_at":
                str(
                    datetime.now()
                )
        }

        approvals.append(
            item
        )

        self.save(
            approvals
        )

        return item

    def approve(
        self,
        approval_id
    ):

        approvals = (
            self.load()
        )

        for item in approvals:

            if (
                item.get(
                    "id"
                )
                ==
                approval_id
            ):

                item[
                    "status"
                ] = "approved"

        self.save(
            approvals)

    def reject(
        self,
        approval_id
    ):

        approvals = (
            self.load()
        )

        for item in approvals:

            if (
                item.get(
                    "id"
                )
                ==
                approval_id
            ):

                item[
                    "status"
                ] = "rejected"

        self.save(
            approvals
        )

    def pending(
        self
    ):

        approvals = (
            self.load()
        )

        return [

            item

            for item in approvals

            if (
                item.get(
                    "status"
                )
                ==
                "pending"
            )
        ]


approval_engine = (
    ApprovalEngine()
)