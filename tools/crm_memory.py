import json
import os

from datetime import (
    datetime
)


CRM_FILE = (
    "memory/crm_memory.json"
)


class CRMMemory:

    def __init__(self):

        self.ensure_memory()

    def ensure_memory(
        self
    ):

        if not os.path.exists(
            CRM_FILE
        ):

            with open(
                CRM_FILE,
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
                CRM_FILE,
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
            CRM_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def find_contact(
        self,
        email
    ):

        contacts = (
            self.load()
        )

        for contact in contacts:

            if (
                contact.get(
                    "email"
                )
                ==
                email
            ):

                return contact

        return None

    def create_contact(
        self,
        email,
        company=""
    ):

        contacts = (
            self.load()
        )

        existing = (
            self.find_contact(
                email
            )
        )

        if existing:

            return existing

        contact = {

            "email":
                email,

            "company":
                company,

            "created_at":
                str(
                    datetime.now()
                ),

            "status":
                "lead",

            "engagement_score":
                0,

            "interactions":
                []
        }

        contacts.append(
            contact
        )

        self.save(
            contacts
        )

        return contact

    def add_interaction(
        self,
        email,
        interaction_type,
        notes=""
    ):

        contacts = (
            self.load()
        )

        for contact in contacts:

            if (
                contact.get(
                    "email"
                )
                ==
                email
            ):

                contact[
                    "interactions"
                ].append(
                    {

                        "type":
                            interaction_type,

                        "notes":
                            notes,

                        "timestamp":
                            str(
                                datetime.now()
                            )
                    }
                )

                contact[
                    "engagement_score"
                ] += 10

        self.save(
            contacts
        )

    def update_status(
        self,
        email,
        status
    ):

        contacts = (
            self.load()
        )

        for contact in contacts:

            if (
                contact.get(
                    "email"
                )
                ==
                email
            ):

                contact[
                    "status"
                ] = status

        self.save(
            contacts
        )

    def top_leads(
        self
    ):

        contacts = (
            self.load()
        )

        sorted_contacts = sorted(

            contacts,

            key=lambda x:
                x.get(
                    "engagement_score",
                    0
                ),

            reverse=True
        )

        return sorted_contacts[:10]


crm_memory = (
    CRMMemory()
)