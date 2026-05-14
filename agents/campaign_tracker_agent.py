import csv
import os
import datetime

# =====================================================
# DATABASE FILE
# =====================================================

CAMPAIGN_DATABASE = (
    "database/campaigns.csv"
)

# =====================================================
# CREATE DATABASE
# =====================================================

def initialize_database():

    if not os.path.exists("database"):

        os.makedirs("database")

    if not os.path.exists(CAMPAIGN_DATABASE):

        with open(
            CAMPAIGN_DATABASE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                "Company",
                "Status",
                "Date",
                "Notes"
            ])

# =====================================================
# ADD CAMPAIGN
# =====================================================

def add_campaign(company, status, notes):

    initialize_database()

    timestamp = str(
        datetime.datetime.now()
    )

    with open(
        CAMPAIGN_DATABASE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            company,
            status,
            timestamp,
            notes
        ])

    print("\nCampaign added successfully.")

# =====================================================
# SHOW CAMPAIGNS
# =====================================================

def show_campaigns():

    initialize_database()

    print("\n================================")
    print("PHANTOMOPS CAMPAIGN TRACKER")
    print("================================\n")

    with open(
        CAMPAIGN_DATABASE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        count = 0

        for row in reader:

            count += 1

            print(f"CAMPAIGN {count}")

            print(f"Company : {row['Company']}")

            print(f"Status  : {row['Status']}")

            print(f"Date    : {row['Date']}")

            print(f"Notes   : {row['Notes']}")

            print("--------------------------------")

        if count == 0:

            print("No campaigns found.")