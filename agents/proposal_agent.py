from agents.base_agent import (
    BaseAgent
)

from tools.proposal_engine import (
    proposal_engine
)

from tools.pdf_proposal_engine import (
    pdf_proposal_engine
)

from tools.telegram_engine import (
    telegram_engine
)


class ProposalAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "ProposalAgent"
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

        telegram_engine.send_message(
            f"PROPOSAL GENERATED\n\n"
            f"{company}\n\n"
            f"PDF Created:\n"
            f"{pdf_path}"
        )

        return {

            "success": True,

            "proposal":
                proposal,

            "pdf":
                pdf_path
        }