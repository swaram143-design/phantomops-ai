from urllib.parse import (
    urlparse
)

from agents.base_agent import (
    BaseAgent
)

from tools.browser_tools import (
    browser_tools
)

from tools.contact_intelligence import (
    contact_intelligence
)

from tools.domain_intelligence import (
    domain_intelligence
)

from tools.decision_intelligence import (
    decision_intelligence
)

from memory.memory_manager import (
    memory_manager
)

from memory.contact_manager import (
    contact_manager
)

from memory.acquisition_memory import (
    acquisition_memory
)


class LeadScraperAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            "LeadScraperAgent"
        )

    def extract_domain(
        self,
        url
    ):

        try:

            return (
                urlparse(url)
                .netloc
                .lower()
            )

        except:

            return ""

    async def execute(self, task):

        description = task.get(
            "description",
            ""
        )

        print(
            f"[LeadScraper] "
            f"Searching: {description}"
        )

        search_results = (
            await browser_tools.search_duckduckgo(
                description
            )
        )

        ranked_results = (
            domain_intelligence.process_results(
                search_results[
                    "results"
                ]
            )
        )

        structured_leads = []

        for result in ranked_results:

            url = result["url"]

            domain = (
                self.extract_domain(
                    url
                )
            )

            if (
                acquisition_memory.has_domain(
                    domain
                )
            ):

                print(
                    f"[LeadScraper] "
                    f"Skipping known domain: "
                    f"{domain}"
                )

                continue

            acquisition_memory.add_domain(
                domain
            )

            print(
                f"[LeadScraper] "
                f"Analyzing: {url}"
            )

            contact_info = (
                await browser_tools.extract_contact_info(
                    url
                )
            )

            processed_emails = (
                contact_intelligence.process_emails(
                    contact_info.get(
                        "emails",
                        []
                    )
                )
            )

            strategic_contacts = (
                decision_intelligence.process_contacts(
                    processed_emails
                )
            )

            filtered_contacts = []

            for contact in (
                strategic_contacts
            ):

                email = contact[
                    "email"
                ]

                if (
                    acquisition_memory.has_contact(
                        email
                    )
                ):

                    continue

                acquisition_memory.add_contact(
                    email
                )

                filtered_contacts.append(
                    contact
                )

            lead = {

                "company":
                    result["title"],

                "website":
                    url,

                "score":
                    result["score"],

                "classification":
                    result[
                        "classification"
                    ],

                "contacts":
                    filtered_contacts
            }

            structured_leads.append(
                lead
            )

            valid_emails = [

                contact["email"]

                for contact in (
                    filtered_contacts
                )
            ]

            if valid_emails:

                contact_manager.add_contact(
                    lead["company"],
                    lead["website"],
                    valid_emails
                )

        memory_manager.add_result(
            structured_leads
        )

        memory_manager.add_event(
            {
                "agent": self.name,
                "action":
                    "memory_centric_acquisition_completed"
            }
        )

        return {
            "success": True,
            "leads":
                structured_leads
        }
