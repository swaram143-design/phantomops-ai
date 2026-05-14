import json
import os
from datetime import (
    datetime
)


CLIENT_MEMORY_FILE = (
    "memory/client_memory.json"
)


class ClientMemory:

    def __init__(self):

        self.ensure_memory()

    def ensure_memory(self):

        if not os.path.exists(
            CLIENT_MEMORY_FILE
        ):

            with open(
                CLIENT_MEMORY_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    {},
                    file,
                    indent=4
                )

    def load(self):

        with open(
            CLIENT_MEMORY_FILE,
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
            CLIENT_MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def remember_project(
        self,
        project
    ):

        data = self.load()

        marketplace = (
            project.get(
                "marketplace",
                "Unknown"
            )
        )

        project_name = (
            project.get(
                "content_preview",
                ""
            )[:80]
        )

        if marketplace not in data:

            data[
                marketplace
            ] = {

                "projects": [],

                "engagements": 0,

                "wins": 0,

                "losses": 0,

                "last_seen": None
            }

        data[
            marketplace
        ][
            "projects"
        ].append(
            {
                "project":
                    project_name,

                "score":
                    project.get(
                        "opportunity_score"
                    ),

                "timestamp":
                    str(
                        datetime.now()
                    )
            }
        )

        data[
            marketplace
        ][
            "engagements"
        ] += 1

        data[
            marketplace
        ][
            "last_seen"
        ] = str(
            datetime.now()
        )

        self.save(
            data
        )

    def record_win(
        self,
        marketplace
    ):

        data = self.load()

        if marketplace in data:

            data[
                marketplace
            ][
                "wins"
            ] += 1

        self.save(
            data
        )

    def record_loss(
        self,
        marketplace
    ):

        data = self.load()

        if marketplace in data:

            data[
                marketplace
            ][
                "losses"
            ] += 1

        self.save(
            data
        )

    def generate_report(
        self
    ):

        data = self.load()

        report = []

        for marketplace, info in (
            data.items()
        ):

            report.append(
                {
                    "marketplace":
                        marketplace,

                    "engagements":
                        info.get(
                            "engagements",
                            0
                        ),

                    "wins":
                        info.get(
                            "wins",
                            0
                        ),

                    "losses":
                        info.get(
                            "losses",
                            0
                        ),

                    "last_seen":
                        info.get(
                            "last_seen"
                        )
                }
            )

        return report


client_memory = (
    ClientMemory()
)