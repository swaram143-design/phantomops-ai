import json
import os


LEARNING_FILE = (
    "memory/learning_memory.json"
)


class LearningEngine:

    def __init__(self):

        self.ensure_memory()

    def ensure_memory(
        self
    ):

        if not os.path.exists(
            LEARNING_FILE
        ):

            default_data = {

                "wins": {},

                "losses": {}
            }

            with open(
                LEARNING_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    default_data,
                    file,
                    indent=4
                )

    def load(
        self
    ):

        try:

            with open(
                LEARNING_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(
                    file
                )

        except:

            return {

                "wins": {},

                "losses": {}
            }

    def save(
        self,
        data
    ):

        with open(
            LEARNING_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def record_win(
        self,
        keywords
    ):

        data = (
            self.load()
        )

        for keyword in keywords:

            current = (
                data["wins"].get(
                    keyword,
                    0
                )
            )

            data["wins"][
                keyword
            ] = current + 1

        self.save(
            data
        )

    def record_loss(
        self,
        keywords
    ):

        data = (
            self.load()
        )

        for keyword in keywords:

            current = (
                data["losses"].get(
                    keyword,
                    0
                )
            )

            data["losses"][
                keyword
            ] = current + 1

        self.save(
            data
        )

    def keyword_boost(
        self,
        keyword
    ):

        data = (
            self.load()
        )

        wins = (
            data["wins"].get(
                keyword,
                0
            )
        )

        losses = (
            data["losses"].get(
                keyword,
                0
            )
        )

        return (

            wins * 5

            -

            losses * 3
        )

    def summary(
        self
    ):

        return self.load()


learning_engine = (
    LearningEngine()
)