from agents.base_agent import (
    BaseAgent
)

from memory.memory_manager import (
    memory_manager
)


class OutreachDraftAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "OutreachDraftAgent"
        )

    async def execute(
        self,
        task
    ):

        company = task.get(
            "company",
            "Company"
        )

        need = task.get(
            "need",
            "automation"
        )

        message = f"""
Hello {company},

I noticed your interest in
{need} solutions.

We specialize in:
- AI automation
- workflow systems
- CRM integrations
- autonomous operations
- intelligent lead generation

We would love to discuss
how automation can help
improve operational efficiency.

Best regards,
PhantomOps AI
"""

        result = {

            "company":
                company,

            "generated_message":
                message
        }

        memory_manager.add_result(
            result
        )

        memory_manager.add_event(
            {
                "agent": self.name,
                "action":
                    "outreach_generated"
            }
        )

        return {
            "success": True,
            "draft":
                result
        }