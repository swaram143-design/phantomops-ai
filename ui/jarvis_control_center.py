import os
import sys
from tools.approval_engine import (
    approval_engine
)


ROOT_DIR = (
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

if ROOT_DIR not in sys.path:

    sys.path.append(
        ROOT_DIR
    )


import streamlit as st

from tools.pipeline_engine import (
    pipeline_engine
)

from tools.crm_memory import (
    crm_memory
)

from tools.campaign_engine import (
    campaign_engine
)

from tools.followup_engine import (
    followup_engine
)


st.set_page_config(

    page_title=
        "Jarvis AI Control Center",

    layout=
        "wide"
)


st.title(
    "Jarvis AI Revenue Operations"
)

st.subheader(
    "Autonomous Commercial Intelligence System"
)


pipeline_summary = (
    pipeline_engine.summary()
)

top_leads = (
    crm_memory.top_leads()
)

campaigns = (
    campaign_engine.load()
)

followups = (
    followup_engine.load()
)


st.header(
    "Revenue Pipeline"
)

col1, col2, col3, col4 = (
    st.columns(4)
)

col1.metric(
    "Discovered",
    pipeline_summary.get(
        "discovered",
        0
    )
)

col2.metric(
    "Engaged",
    pipeline_summary.get(
        "engaged",
        0
    )
)

col3.metric(
    "Negotiation",
    pipeline_summary.get(
        "negotiation",
        0
    )
)

col4.metric(
    "Won",
    pipeline_summary.get(
        "won",
        0
    )
)


st.divider()


st.header(
    "Top Leads"
)

if top_leads:

    for lead in top_leads:

        with st.container():

            st.subheader(
                lead.get(
                    "email",
                    "Unknown"
                )
            )

            st.write(
                f"Status: "
                f"{lead.get('status')}"
            )

            st.write(
                f"Engagement Score: "
                f"{lead.get('engagement_score')}"
            )

            st.write(
                f"Interactions: "
                f"{len(lead.get('interactions', []))}"
            )

            st.divider()

else:

    st.info(
        "No leads available."
    )


st.header(
    "Campaign Intelligence"
)

if campaigns:

    for campaign in campaigns:

        with st.container():

            st.subheader(
                campaign.get(
                    "name",
                    "Unnamed Campaign"
                )
            )

            st.write(
                f"Targets: "
                f"{len(campaign.get('targets', []))}"
            )

            st.write(
                f"Responses: "
                f"{campaign.get('responses', 0)}"
            )

            st.write(
                f"Created: "
                f"{campaign.get('created_at')}"
            )

            st.divider()

else:

    st.info(
        "No campaigns available."
    )


st.header(
    "Autonomous Followups"
)

if followups:

    for item in followups:

        with st.container():

            st.subheader(
                item.get(
                    "email"
                )
            )

            st.write(
                f"Company: "
                f"{item.get('company')}"
            )

            st.write(
                f"Attempts: "
                f"{item.get('attempts')}"
            )

            st.write(
                f"Status: "
                f"{item.get('status')}"
            )

            st.write(
                f"Next Followup: "
                f"{item.get('next_followup')}"
            )

            st.divider()

else:

    st.info(
        "No followups scheduled."
    )


st.header(
    "Jarvis Runtime Status"
)

st.success(
    "PhantomOps Runtime Active"
)

st.write(
    "Inbox Intelligence: ACTIVE"
)

st.write(
    "CRM Memory: ACTIVE"
)

st.write(
    "Revenue Pipeline: ACTIVE"
)

st.write(
    "Autonomous Followups: ACTIVE"
)

st.write(
    "Telegram Alerts: ACTIVE"
)

st.write(
    "Commercial Intelligence: ACTIVE"
)
st.header(
    "Approval Queue"
)

pending = (
    approval_engine.pending()
)

if pending:

    for item in pending:

        project = (
            item.get(
                "project",
                {}
            )
        )

        with st.container():

            st.subheader(
                project.get(
                    "title"
                )
            )

            st.write(
                f"Client: "
                f"{project.get('client')}"
            )

            st.write(
                f"Score: "
                f"{item.get('score')}"
            )

            st.write(
                f"Approval ID: "
                f"{item.get('id')}"
            )

            st.text_area(
                "Generated Bid",
                item.get(
                    "bid"
                ),
                height=200
            )

            st.divider()

else:

    st.info(
        "No pending approvals."
    )