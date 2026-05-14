import json
import os

from datetime import (
    datetime
)

from tools.learning_engine import (
    learning_engine
)


QUEUE_FILE = (
    "memory/approval_queue.json"
)


class ApprovalQueue:

    def __init__(self):

        self.ensure_file()

    def ensure_file(self):

        if not os.path.exists(
            QUEUE_FILE
        ):

            with open(
                QUEUE_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

    def load(self):

        with open(
            QUEUE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    def save(
        self,
        data
    ):

        with open(
            QUEUE_FILE,
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
        project
    ):

        data = self.load()

        project[
            "approval_status"
        ] = "pending"

        project[
            "created_at"
        ] = str(
            datetime.now()
        )

        data.append(
            project
        )

        self.save(
            data
        )

    def approve(
        self,
        index
    ):

        data = self.load()

        if index < len(data):

            data[index][
                "approval_status"
            ] = "approved"

            data[index][
                "approved_at"
            ] = str(
                datetime.now()
            )

        self.save(
            data
        )

    def reject(
        self,
        index
    ):

        data = self.load()

        if index < len(data):

            data[index][
                "approval_status"
            ] = "rejected"

            learning_engine.record_loss(
                data[index]
            )

        self.save(
            data
        )

    def mark_submitted(
        self,
        index
    ):

        data = self.load()

        if index < len(data):

            data[index][
                "submission_status"
            ] = "submitted"

            data[index][
                "submitted_at"
            ] = str(
                datetime.now()
            )

        self.save(
            data
        )

    def mark_won(
        self,
        index
    ):

        data = self.load()

        if index < len(data):

            data[index][
                "deal_result"
            ] = "won"

            learning_engine.record_win(
                data[index]
            )

        self.save(
            data
        )

    def mark_lost(
        self,
        index
    ):

        data = self.load()

        if index < len(data):

            data[index][
                "deal_result"
            ] = "lost"

            learning_engine.record_loss(
                data[index]
            )

        self.save(
            data
        )


approval_queue = (
    ApprovalQueue()
)