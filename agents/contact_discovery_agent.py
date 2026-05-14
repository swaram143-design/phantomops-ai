import csv
import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

# =====================================================
# FILES
# =====================================================

INPUT_DATABASE = (
    "database/clean_leads.csv"
)

OUTPUT_DATABASE = (
    "database/contacts.csv"
)

# =====================================================
# EMAIL REGEX
# =====================================================

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+"

# =====================================================
# LOAD LEADS
# =====================================================

def load_leads():

    leads = []

    with open(
        INPUT_DATABASE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            leads.append(row)

    return leads

# =====================================================
# SAVE CONTACT
# =====================================================

def save_contact(domain, page, email):

    with open(
        OUTPUT_DATABASE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            domain,
            page,
            email
        ])

# =====================================================
# FIND CONTACT PAGES
# =====================================================

def discover_contact_pages(url):

    pages = []

    try:

        headers = {

            "User-Agent":
            "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = soup.find_all("a")

        for link in links:

            href = link.get("href")

            if href:

                text = href.lower()

                if (
                    "contact" in text
                    or "about" in text
                    or "support" in text
                ):

                    full_url = urljoin(
                        url,
                        href
                    )

                    pages.append(full_url)

    except:
        pass

    return list(set(pages))

# =====================================================
# EXTRACT EMAILS
# =====================================================

def extract_emails(url):

    try:

        headers = {

            "User-Agent":
            "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text()

        emails = re.findall(
            email_pattern,
            text
        )

        return list(set(emails))

    except:

        return []

# =====================================================
# MAIN ENGINE
# =====================================================

def discover_contacts():

    leads = load_leads()

    # =============================================
    # CREATE OUTPUT FILE
    # =============================================

    with open(
        OUTPUT_DATABASE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Domain",
            "Page",
            "Email"
        ])

    print("\n================================")
    print("CONTACT PAGE DISCOVERY ENGINE")
    print("================================\n")

    # =============================================
    # PROCESS LEADS
    # =============================================

    for index, lead in enumerate(leads, start=1):

        domain = lead["Domain"]

        website = lead["Website"]

        print(f"\nLEAD {index}")

        print(f"Website: {website}")

        # =========================================
        # FIND CONTACT PAGES
        # =========================================

        pages = discover_contact_pages(
            website
        )

        if len(pages) == 0:

            print("No contact pages found.")

            continue

        # =========================================
        # SCAN CONTACT PAGES
        # =========================================

        for page in pages:

            print(f"\nScanning: {page}")

            emails = extract_emails(page)

            if len(emails) == 0:

                print("No emails found.")

            else:

                for email in emails:

                    print(f"Found: {email}")

                    save_contact(
                        domain,
                        page,
                        email
                    )

    print("\nContact discovery completed.")