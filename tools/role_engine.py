class RoleEngine:

    def __init__(self):

        self.roles = {

            "buyer": [

                "hiring",
                "need",
                "looking for",
                "seeking",
                "developer jobs",
                "consultant needed",
                "specialist"
            ],

            "competitor": [

                "agency",
                "consulting",
                "services",
                "solutions",
                "experts",
                "automation company",
                "consultants"
            ],

            "marketplace": [

                "freelance jobs",
                "projects",
                "earn online",
                "work remote",
                "hire freelancers"
            ],

            "tool_provider": [

                "platform",
                "software",
                "tool",
                "app",
                "saas",
                "workflow platform"
            ],

            "informational": [

                "guide",
                "tutorial",
                "tips",
                "blog",
                "examples",
                "top 10",
                "comparison"
            ]
        }

    def analyze_role(
        self,
        title
    ):

        title = title.lower()

        scores = {}

        for role, phrases in (
            self.roles.items()
        ):

            score = 0

            for phrase in phrases:

                if phrase in title:

                    score += 20

            scores[role] = score

        best_role = max(
            scores,
            key=scores.get
        )

        return {
            "role": best_role,
            "scores": scores
        }

    def determine_action(
        self,
        role
    ):

        actions = {

            "buyer":
                "prioritize_outreach",

            "competitor":
                "monitor_market",

            "marketplace":
                "mine_opportunities",

            "tool_provider":
                "potential_partnership",

            "informational":
                "ignore"
        }

        return actions.get(
            role,
            "observe"
        )

    def process(
        self,
        opportunities
    ):

        processed = []

        for item in opportunities:

            title = item.get(
                "title",
                ""
            )

            analysis = (
                self.analyze_role(
                    title
                )
            )

            role = analysis[
                "role"
            ]

            if role == "informational":

                continue

            item[
                "commercial_role"
            ] = role

            item[
                "recommended_action"
            ] = (
                self.determine_action(
                    role
                )
            )

            item[
                "role_scores"
            ] = analysis[
                "scores"
            ]

            processed.append(
                item
            )

        processed.sort(
            key=lambda x: (
                x.get(
                    "entity_score",
                    0
                )
                +
                x.get(
                    "score",
                    0
                )
            ),
            reverse=True
        )

        return processed


role_engine = (
    RoleEngine()
)