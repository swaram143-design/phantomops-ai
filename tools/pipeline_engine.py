import json
import os

from datetime import (
    datetime
)


PIPELINE_FILE = (
    "memory/pipeline.json"
)


class PipelineEngine:

    def __init__(self):

        self.ensure_memory()

    def ensure_memory(
        self
    ):

        if not os.path.exists(
            PIPELINE_FILE
        ):

            with open(
                PIPELINE_FILE,
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
                PIPELINE_FILE,
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
            PIPELINE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def create_opportunity(
        self,
        email,
        company,
        stage="discovered"
    ):

        pipeline = (
            self.load()
        )

        existing = None

        for item in pipeline:

            if (
                item.get(
                    "email"
                )
                ==
                email
            ):

                existing = item

        if existing:

            return existing

        opportunity = {

            "email":
                email,

            "company":
                company,

            "stage":
                stage,

            "created_at":
                str(
                    datetime.now()
                ),

            "updated_at":
                str(
                    datetime.now()
                ),

            "history":
                []
        }

        pipeline.append(
            opportunity
        )

        self.save(
            pipeline
        )

        return opportunity

    def update_stage(
        self,
        email,
        new_stage,
        notes=""
    ):

        pipeline = (
            self.load()
        )

        for item in pipeline:

            if (
                item.get(
                    "email"
                )
                ==
                email
            ):

                old_stage = (
                    item.get(
                        "stage"
                    )
                )

                item[
                    "stage"
                ] = new_stage

                item[
                    "updated_at"
                ] = str(
                    datetime.now()
                )

                item[
                    "history"
                ].append(
                    {

                        "from":
                            old_stage,

                        "to":
                            new_stage,

                        "notes":
                            notes,

                        "timestamp":
                            str(
                                datetime.now()
                            )
                    }
                )

        self.save(
            pipeline
        )

    def get_pipeline(
        self
    ):

        return self.load()

    def summary(
        self
    ):

        pipeline = (
            self.load()
        )

        summary = {

            "discovered": 0,
            "contacted": 0,
            "engaged": 0,
            "meeting": 0,
            "proposal": 0,
            "negotiation": 0,
            "won": 0,
            "lost": 0
        }

        for item in pipeline:

            stage = (
                item.get(
                    "stage"
                )
            )

            if stage in summary:

                summary[
                    stage
                ] += 1

        return summary


pipeline_engine = (
    PipelineEngine()
)