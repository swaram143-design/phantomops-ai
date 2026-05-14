from agents.base_agent import (
    BaseAgent
)

from tools.proposal_engine import (
    proposal_engine
)

from tools.pdf_proposal_engine import (
    pdf_proposal_engine
)

from tools.email_tool import (
    email_tool
)

from tools.telegram_engine import (
    telegram_engine
)

from tools.pipeline_engine import (
    pipeline_engine
)


class ProposalDeliveryAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "ProposalDeliveryAgent"
        )

    async def execute(
        self,
        task
    ):

        company = (
            task.get(
                "company",
                "Unknown Client"
            )
        )

        need = (
            task.get(
                "need",
                "automation"
            )
        )

        recipient = (
            task.get(
                "recipient"
            )
        )

        proposal = (
            proposal_engine.generate_proposal(
                company,
                need
            )
        )

        pdf_path = (
            pdf_proposal_engine.generate_pdf(
                company,
                proposal
            )
        )

        subject = (
            f"Automation Proposal for {company}"
        )

        body = f"""
Hello {company},

Attached is your requested
automation proposal document.

The proposal includes:
- workflow automation
- CRM integration
- lead generation systems
- revenue operations intelligence

Please review the attached PDF.

Best regards,
PhantomOps AI
"""

        result = (
            email_tool.send_email(
                recipient,
                subject,
                body,
                attachment_path=pdf_path
            )
        )

        if result.get(
            "success"
        ):

            pipeline_engine.create_opportunity(
                recipient,
                company
            )

            pipeline_engine.update_stage(
                recipient,
                "proposal",
                "Proposal delivered"
            )

            telegram_engine.send_message(
                f"PROPOSAL DELIVERED\n\n"
                f"{company}\n\n"
                f"{recipient}"
            )

        else:

            telegram_engine.send_message(
                f"PROPOSAL DELIVERY FAILED\n\n"
                f"{recipient}\n\n"
                f"{result.get('error')}"
            )

        return {

            "success":
                result.get(
                    "success"
                ),

            "error":
                result.get(
                    "error"
                ),

            "pdf":
                pdf_path,

            "recipient":
                recipient
        }