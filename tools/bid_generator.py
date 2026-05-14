class BidGenerator:

    def generate_bid(
        self,
        title,
        description
    ):

        bid = f"""
Hello,

I reviewed your project:

{title}

Your requirements align strongly
with our AI automation expertise.

We specialize in:
- workflow automation
- CRM systems
- AI agents
- lead generation
- autonomous business operations

We can build:
- scalable automation systems
- intelligent workflows
- AI-powered integrations
- operational dashboards

Why choose us?
- rapid delivery
- AI-first infrastructure
- autonomous operations expertise
- scalable architecture

We would be happy to discuss:
- project scope
- timeline
- implementation plan
- optimization opportunities

Best regards,
PhantomOps AI
"""

        return bid


bid_generator = (
    BidGenerator()
)