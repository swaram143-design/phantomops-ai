from datetime import datetime


class ProposalEngine:
    """Generate the low-friction PhantomOps revenue pilot offer."""

    PILOT_PRICE = "₹9,999"
    MONTHLY_PRICE = "₹19,999–₹29,999/month"

    def generate_proposal(self, company, need):
        company = company or "Prospect"
        need = need or "lead generation and follow-up automation"

        return f"""PHANTOMOPS AI
7-DAY LEAD AUTOMATION PILOT

Prepared: {datetime.now():%Y-%m-%d}

Prospect:
{company}

Business Need:
{need}

WHAT WE WILL DO
- Find and qualify relevant prospects
- Prepare personalized outreach for qualified prospects
- Capture prospects in a simple CRM pipeline
- Set up follow-up automation
- Operate the pilot campaign for 7 days
- Provide campaign results and next-step recommendations

YOUR APPROVAL CONTROL
No external outreach is sent without your approval.

PILOT INVESTMENT
{self.PILOT_PRICE} one-time

AFTER THE PILOT
If the pilot produces useful results, managed automation is available at
{self.MONTHLY_PRICE}, depending on campaign volume and scope.

EXPECTED START
Configuration can begin after approval and payment.

Prepared by:
PhantomOps AI
"""


proposal_engine = ProposalEngine()
