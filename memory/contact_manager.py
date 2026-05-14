import json
import os

from datetime import datetime


class ContactManager:

    def __init__(self):

        self.contacts_path = (
            "memory/contacts.json"
        )

        self.data = {
            "contacts": []
        }

        self.load_contacts()

    def load_contacts(self):

        if os.path.exists(
            self.contacts_path
        ):

            with open(
                self.contacts_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.data = json.load(file)

    def save_contacts(self):

        with open(
            self.contacts_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.data,
                file,
                indent=4
            )

    def add_contact(
        self,
        company,
        website,
        emails
    ):

        contact = {
            "timestamp":
                str(datetime.now()),
            "company":
                company,
            "website":
                website,
            "emails":
                emails,
            "status":
                "new"
        }

        self.data[
            "contacts"
        ].append(contact)

        self.save_contacts()

    def get_contacts(self):

        return self.data[
            "contacts"
        ]


contact_manager = ContactManager()