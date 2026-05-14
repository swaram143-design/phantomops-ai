import re


class ProjectIntelligence:

    def __init__(self):

        self.high_value_keywords = [

            "enterprise",
            "healthcare",
            "crm",
            "automation",
            "integration",
            "workflow",
            "ai",
            "api",
            ".net",
            "edi"
        ]

        self.urgency_keywords = [

            "urgent",
            "asap",
            "immediately",
            "quickly",
            "fast",
            "deadline"
        ]

    def extract_budget(
        self,
        text
    ):

        matches = re.findall(
            r"\$[\d,.]+",
            text
        )

        return matches[:5]

    def detect_skills(
        self,
        text
    ):

        text = text.lower()

        found = []

        for keyword in (
            self.high_value_keywords
        ):

            if keyword in text:

                found.append(
                    keyword
                )

        return list(
            set(found)
        )

    def detect_urgency(
        self,
        text
    ):

        text = text.lower()

        for keyword in (
            self.urgency_keywords
        ):

            if keyword in text:

                return "high"

        return "normal"

    def estimate_value(
        self,
        skills,
        budgets
    ):

        score = 0

        score += (
            len(skills) * 10
        )

        score += (
            len(budgets) * 20
        )

        if score >= 80:

            return "high_ticket"

        if score >= 40:

            return "medium_value"

        return "low_value"

    def analyze_project(
        self,
        content
    ):

        budgets = (
            self.extract_budget(
                content
            )
        )

        skills = (
            self.detect_skills(
                content
            )
        )

        urgency = (
            self.detect_urgency(
                content
            )
        )

        estimated_value = (
            self.estimate_value(
                skills,
                budgets
            )
        )

        return {

            "budgets":
                budgets,

            "skills":
                skills,

            "urgency":
                urgency,

            "estimated_value":
                estimated_value
        }

    def process(
        self,
        projects
    ):

        processed = []

        for item in projects:

            content = item.get(
                "content_preview",
                ""
            )

            analysis = (
                self.analyze_project(
                    content
                )
            )

            item[
                "project_analysis"
            ] = analysis

            processed.append(
                item
            )

        return processed


project_intelligence = (
    ProjectIntelligence()
)