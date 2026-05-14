class OpportunityScoring:

    def __init__(self):

        self.high_value_skills = [

            "healthcare",
            "edi",
            "api",
            "automation",
            "workflow",
            ".net",
            "integration",
            "ai"
        ]

    def calculate_skill_score(
        self,
        skills
    ):

        score = 0

        for skill in skills:

            if skill in (
                self.high_value_skills
            ):

                score += 10

        return score

    def calculate_budget_score(
        self,
        budgets
    ):

        if not budgets:

            return 10

        return min(
            len(budgets) * 15,
            40
        )

    def calculate_urgency_score(
        self,
        urgency
    ):

        if urgency == "high":

            return 20

        return 5

    def calculate_complexity(
        self,
        skills
    ):

        if len(skills) >= 6:

            return "high"

        if len(skills) >= 3:

            return "medium"

        return "low"

    def determine_priority(
        self,
        total_score
    ):

        if total_score >= 80:

            return "priority_bid"

        if total_score >= 50:

            return "recommended"

        return "low_priority"

    def process_project(
        self,
        item
    ):

        analysis = item.get(
            "project_analysis",
            {}
        )

        skills = analysis.get(
            "skills",
            []
        )

        budgets = analysis.get(
            "budgets",
            []
        )

        urgency = analysis.get(
            "urgency",
            "normal"
        )

        skill_score = (
            self.calculate_skill_score(
                skills
            )
        )

        budget_score = (
            self.calculate_budget_score(
                budgets
            )
        )

        urgency_score = (
            self.calculate_urgency_score(
                urgency
            )
        )

        total_score = (
            skill_score
            +
            budget_score
            +
            urgency_score
        )

        complexity = (
            self.calculate_complexity(
                skills
            )
        )

        priority = (
            self.determine_priority(
                total_score
            )
        )

        item[
            "opportunity_score"
        ] = total_score

        item[
            "complexity"
        ] = complexity

        item[
            "priority_action"
        ] = priority

        return item

    def process(
        self,
        projects
    ):

        processed = []

        for item in projects:

            scored = (
                self.process_project(
                    item
                )
            )

            processed.append(
                scored
            )

        processed.sort(
            key=lambda x: (
                x.get(
                    "opportunity_score",
                    0
                )
            ),
            reverse=True
        )

        return processed


opportunity_scoring = (
    OpportunityScoring()
)