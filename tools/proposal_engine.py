from datetime import (
    datetime
)


class ProposalEngine:

    def __init__(self):

        self.base_services = [

            {
                "name":
                    "AI Automation System",

                "price":
                    "$1500"
            },

            {
                "name":
                    "CRM Integration",

                "price":
                    "$800"
            },

            {
                "name":
                    "Lead Generation Automation",

                "price":
                    "$1200"
            },

            {
                "name":
                    "Autonomous Workflow System",

                "price":
                    "$2000"
            }
        ]

    def generate_proposal(
        self,
        company,
        need
    ):

        services = []

        total = 0

        for service in (
            self.base_services
        ):

            if (

                "automation"
                in need.lower()

                or

                "workflow"
                in need.lower()

            ):

                services.append(
                    service
                )

                price = int(

                    service[
                        "price"
                    ].replace(
                        "$",
                        ""
                    )
                )

                total += price

        proposal = f"""
PHANTOMOPS AI
Automation Proposal

Generated:
{datetime.now()}

Client:
{company}

Project Need:
{need}

Recommended Services:
"""

        for service in services:

            proposal += f"""

- {service['name']}
  Estimated Price:
  {service['price']}
"""

        proposal += f"""

Estimated Total:
${total}

Implementation Includes:
- AI workflow automation
- CRM integrations
- lead management systems
- autonomous followups
- revenue pipeline intelligence

Timeline:
2-4 weeks

Prepared by:
PhantomOps AI
"""

        return proposal


proposal_engine = (
    ProposalEngine()
)