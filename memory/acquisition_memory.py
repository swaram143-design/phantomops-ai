import json
import os


class AcquisitionMemory:

    def __init__(self):

        self.path = (
            "memory/acquisition_memory.json"
        )

        self.data = {

            "domains": [],

            "contacts": [],

            "campaigns": []
        }

        self.load()

    def load(self):

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

    def save(self):

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

    def has_domain(
        self,
        domain
    ):

        return (
            domain in
            self.data["domains"]
        )

    def add_domain(
        self,
        domain
    ):

        if not self.has_domain(
            domain
        ):

            self.data[
                "domains"
            ].append(domain)

            self.save()

    def has_contact(
        self,
        email
    ):

        return (
            email in
            self.data["contacts"]
        )

    def add_contact(
        self,
        email
    ):

        if not self.has_contact(
            email
        ):

            self.data[
                "contacts"
            ].append(email)

            self.save()

    def has_campaign(
        self,
        email
    ):

        return (
            email in
            self.data["campaigns"]
        )

    def add_campaign(
        self,
        email
    ):

        if not self.has_campaign(
            email
        ):

            self.data[
                "campaigns"
            ].append(email)

            self.save()


acquisition_memory = (
    AcquisitionMemory()
)