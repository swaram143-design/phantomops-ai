import json
import os

from datetime import datetime


class CampaignManager:

    def __init__(self):

        self.path = (
            "memory/campaigns.json"
        )

        self.data = {
            "campaigns": []
        }

        self.load_campaigns()

    def load_campaigns(self):

        if os.path.exists(
            self.path
        ):

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:

                self.data = json.load(
                    file
                )

    def save_campaigns(self):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.data,
                file,
                indent=4
            )

    def create_campaign(
        self,
        company,
        email,
        message
    ):

        campaign = {

            "timestamp":
                str(datetime.now()),

            "company":
                company,

            "email":
                email,

            "message":
                message,

            "status":
                "pending_review"
        }

        self.data[
            "campaigns"
        ].append(campaign)

        self.save_campaigns()

    def get_campaigns(self):

        return self.data[
            "campaigns"
        ]

    def approve_campaign(
        self,
        index
    ):

        if (
            index <
            len(
                self.data[
                    "campaigns"
                ]
            )
        ):

            self.data[
                "campaigns"
            ][index][
                "status"
            ] = "approved"

            self.save_campaigns()

    def mark_sent(
        self,
        index
    ):

        if (
            index <
            len(
                self.data[
                    "campaigns"
                ]
            )
        ):

            self.data[
                "campaigns"
            ][index][
                "status"
            ] = "sent"

            self.save_campaigns()


campaign_manager = CampaignManager()