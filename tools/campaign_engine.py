import json
import os

from datetime import (
    datetime
)


CAMPAIGN_FILE = (
    "memory/campaigns.json"
)


class CampaignEngine:

    def __init__(self):

        self.ensure_memory()

    def ensure_memory(self):

        if not os.path.exists(
            CAMPAIGN_FILE
        ):

            with open(
                CAMPAIGN_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

    def load(self):

        try:

            with open(
                CAMPAIGN_FILE,
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
            CAMPAIGN_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def create_campaign(
        self,
        name,
        targets
    ):

        campaigns = (
            self.load()
        )

        campaign = {

            "name":
                name,

            "created_at":
                str(
                    datetime.now()
                ),

            "targets":
                targets,

            "emails_sent":
                0,

            "responses":
                0,

            "wins":
                0,

            "status":
                "active"
        }

        campaigns.append(
            campaign
        )

        self.save(
            campaigns
        )

        return campaign

    def increment_sent(
        self,
        campaign_name
    ):

        campaigns = (
            self.load()
        )

        for campaign in campaigns:

            if (
                campaign.get(
                    "name"
                )
                ==
                campaign_name
            ):

                campaign[
                    "emails_sent"
                ] += 1

        self.save(
            campaigns
        )

    def increment_response(
        self,
        campaign_name
    ):

        campaigns = (
            self.load()
        )

        for campaign in campaigns:

            if (
                campaign.get(
                    "name"
                )
                ==
                campaign_name
            ):

                campaign[
                    "responses"
                ] += 1

        self.save(
            campaigns
        )

    def increment_win(
        self,
        campaign_name
    ):

        campaigns = (
            self.load()
        )

        for campaign in campaigns:

            if (
                campaign.get(
                    "name"
                )
                ==
                campaign_name
            ):

                campaign[
                    "wins"
                ] += 1

        self.save(
            campaigns
        )


campaign_engine = (
    CampaignEngine()
)