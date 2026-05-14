import csv

# =====================================================
# FILES
# =====================================================

INPUT_DATABASE = (
    "database/clean_leads.csv"
)

OUTPUT_DATABASE = (
    "database/scored_leads.csv"
)

# =====================================================
# HIGH VALUE KEYWORDS
# =====================================================

high_value_keywords = [

    "ai",
    "automation",
    "agency",
    "software",
    "tech",
    "cloud",
    "digital",
    "enterprise",
    "saas",
    "intelligence"
]

# =====================================================
# SCORE LEAD
# =====================================================

def calculate_score(domain, website):

    score = 0

    text = (
        domain.lower() +
        website.lower()
    )

    # =============================================
    # KEYWORD SCORING
    # =============================================

    for keyword in high_value_keywords:

        if keyword in text:

            score += 10

    # =============================================
    # HTTPS BONUS
    # =============================================

    if website.startswith("https"):

        score += 10

    # =============================================
    # DOMAIN LENGTH BONUS
    # =============================================

    if len(domain) < 25:

        score += 5

    return score

# =====================================================
# LEAD CATEGORY
# =====================================================

def categorize_lead(score):

    if score >= 40:

        return "HIGH VALUE"

    elif score >= 20:

        return "MEDIUM VALUE"

    else:

        return "LOW VALUE"

# =====================================================
# PROCESS LEADS
# =====================================================

def score_leads():

    scored = []

    with open(
        INPUT_DATABASE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            domain = row["Domain"]

            website = row["Website"]

            score = calculate_score(
                domain,
                website
            )

            category = categorize_lead(
                score
            )

            scored.append([

                domain,
                website,
                score,
                category
            ])

    # =============================================
    # SORT BY SCORE
    # =============================================

    scored.sort(
        key=lambda x: x[2],
        reverse=True
    )

    # =============================================
    # SAVE DATABASE
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
            "Website",
            "Score",
            "Category"
        ])

        for item in scored:

            writer.writerow(item)

    # =============================================
    # DISPLAY RESULTS
    # =============================================

    print("\n================================")
    print("LEAD SCORING ENGINE")
    print("================================\n")

    for index, item in enumerate(scored, start=1):

        print(f"{index}. {item[0]}")

        print(f"   Score    : {item[2]}")

        print(f"   Category : {item[3]}")

        print(f"   Website  : {item[1]}\n")

    print(
        f"{len(scored)} leads scored."
    )