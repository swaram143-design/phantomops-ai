import csv

from urllib.parse import urlparse

# =====================================================
# FILES
# =====================================================

RAW_DATABASE = (
    "database/leads.csv"
)

CLEAN_DATABASE = (
    "database/clean_leads.csv"
)

# =====================================================
# BLOCKED WORDS
# =====================================================

blocked_words = [

    "blog",
    "rank",
    "top-",
    "directory",
    "hub",
    "list",
    "article",
    "news"
]

# =====================================================
# EXTRACT DOMAIN
# =====================================================

def extract_domain(url):

    try:

        parsed = urlparse(url)

        domain = parsed.netloc

        domain = domain.replace(
            "www.",
            ""
        )

        return domain

    except:

        return None

# =====================================================
# CHECK QUALITY
# =====================================================

def is_valid_lead(title, website):

    text = (
        title.lower() +
        website.lower()
    )

    for word in blocked_words:

        if word in text:

            return False

    return True

# =====================================================
# CLEAN LEADS
# =====================================================

def clean_leads():

    cleaned = []

    with open(
        RAW_DATABASE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            title = row["Title"]

            website = row["Website"]

            # =========================================
            # FILTER RESULTS
            # =========================================

            if is_valid_lead(
                title,
                website
            ):

                domain = extract_domain(
                    website
                )

                if domain:

                    cleaned.append([
                        domain,
                        website
                    ])

    # =============================================
    # SAVE CLEAN DATABASE
    # =============================================

    with open(
        CLEAN_DATABASE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Domain",
            "Website"
        ])

        for item in cleaned:

            writer.writerow(item)

    # =============================================
    # DISPLAY RESULTS
    # =============================================

    print("\n================================")
    print("CLEAN LEAD DATABASE")
    print("================================\n")

    for index, item in enumerate(cleaned, start=1):

        print(f"{index}. {item[0]}")

        print(f"   {item[1]}\n")

    print(
        f"{len(cleaned)} clean leads saved."
    )