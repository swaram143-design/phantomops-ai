class PipelineIntelligence:

    def __init__(self):

        self.stage_keywords = {

            "meeting": [

                "meeting",
                "schedule",
                "calendar",
                "zoom",
                "call"
            ],

            "proposal": [

                "proposal",
                "quotation",
                "document",
                "scope",
                "presentation"
            ],

            "negotiation": [

                "pricing",
                "contract",
                "budget",
                "cost",
                "payment"
            ],

            "won": [

                "approved",
                "confirmed",
                "let us proceed",
                "deal",
                "start project"
            ]
        }

    def detect_stage(
        self,
        subject,
        body
    ):

        combined = (
            (
                subject
                +
                " "
                +
                body
            ).lower()
        )

        for stage, keywords in (
            self.stage_keywords.items()
        ):

            for keyword in keywords:

                if keyword in combined:

                    return stage

        return None


pipeline_intelligence = (
    PipelineIntelligence()
)