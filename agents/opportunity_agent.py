from agents.base_agent import (
    BaseAgent
)

from tools.browser_tools import (
    browser_tools
)

from tools.opportunity_intelligence import (
    opportunity_intelligence
)

from tools.buyer_intent import (
    buyer_intent
)

from tools.entity_intelligence import (
    entity_intelligence
)

from tools.context_engine import (
    context_engine
)

from tools.role_engine import (
    role_engine
)

from tools.directional_engine import (
    directional_engine
)

from tools.strategic_engine import (
    strategic_engine
)

from tools.execution_engine import (
    execution_engine
)

from memory.memory_manager import (
    memory_manager
)


class OpportunityAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "OpportunityAgent"
        )

        self.discovery_queries = [

            "need AI automation help",

            "hiring workflow automation expert",

            "looking for AI chatbot developer",

            "CRM automation freelancer",

            "business automation consultant",

            "AI workflow project",

            "automation engineer freelance",

            "need AI integrations"
        ]

    async def execute(self, task):

        all_results = []

        for query in (
            self.discovery_queries
        ):

            print(
                f"[OpportunityAgent] "
                f"Searching: {query}"
            )

            search_results = (
                await browser_tools.search_duckduckgo(
                    query
                )
            )

            processed = (
                opportunity_intelligence.process_results(
                    search_results[
                        "results"
                    ]
                )
            )

            all_results.extend(
                processed
            )

        buyer_ranked = (
            buyer_intent.process(
                all_results
            )
        )

        entity_ranked = (
            entity_intelligence.process(
                buyer_ranked
            )
        )

        semantic_ranked = (
            context_engine.process(
                entity_ranked
            )
        )

        role_ranked = (
            role_engine.process(
                semantic_ranked
            )
        )

        directional_ranked = (
            directional_engine.process(
                role_ranked
            )
        )

        strategic_ranked = (
            strategic_engine.process(
                directional_ranked
            )
        )

        execution_ranked = (
            execution_engine.process(
                strategic_ranked
            )
        )

        memory_manager.add_result(
            execution_ranked
        )

        memory_manager.add_event(
            {
                "agent": self.name,
                "action":
                    "execution_reasoning_completed"
            }
        )

        return {
            "success": True,
            "opportunities":
                execution_ranked
        }