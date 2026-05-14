import sys
import os

import pandas as pd
import streamlit as st

from tools.campaign_engine import (
    campaign_engine
)


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from memory.approval_queue import (
    approval_queue
)

from memory.client_memory import (
    client_memory
)

from tools.learning_engine import (
    learning_engine
)


st.set_page_config(
    page_title="PhantomOps Command Center",
    layout="wide"
)


st.title(
    "PhantomOps AI Revenue Operations"
)


projects = (
    approval_queue.load()
)


st.sidebar.header(
    "Filters"
)

minimum_score = (
    st.sidebar.slider(
        "Minimum Score",
        0,
        150,
        0
    )
)

priority_filter = (
    st.sidebar.selectbox(
        "Priority",
        [
            "all",
            "priority_bid",
            "recommended",
            "low_priority"
        ]
    )
)

healthcare_only = (
    st.sidebar.checkbox(
        "Healthcare Only"
    )
)


filtered = []

for item in projects:

    score = item.get(
        "opportunity_score",
        0
    )

    priority = item.get(
        "priority_action",
        ""
    )

    skills = (
        item.get(
            "project_analysis",
            {}
        ).get(
            "skills",
            []
        )
    )

    if (
        score
        <
        minimum_score
    ):

        continue

    if (
        priority_filter
        !=
        "all"
        and
        priority
        !=
        priority_filter
    ):

        continue

    if (
        healthcare_only
        and
        "healthcare"
        not in skills
    ):

        continue

    filtered.append(
        item
    )


st.subheader(
    "Revenue Opportunities"
)

summary = []

for item in filtered:

    summary.append(
        {
            "Marketplace":
                item.get(
                    "marketplace"
                ),

            "Score":
                item.get(
                    "opportunity_score"
                ),

            "Priority":
                item.get(
                    "priority_action"
                ),

            "Stage":
                item.get(
                    "deal_stage"
                ),

            "Probability":
                item.get(
                    "close_probability"
                ),

            "Deal Value":
                item.get(
                    "estimated_deal_value"
                ),

            "Approval":
                item.get(
                    "approval_status"
                )
        }
    )

if summary:

    dataframe = (
        pd.DataFrame(
            summary
        )
    )

    st.dataframe(
        dataframe,
        use_container_width=True
    )

else:

    st.warning(
        "No matching opportunities."
    )


st.subheader(
    "Approval Queue"
)

for index, item in enumerate(
    filtered
):

    with st.expander(
        f"{index + 1}. "
        f"{item.get('marketplace')} "
        f"| "
        f"{item.get('approval_status')}"
    ):

        st.write(
            "Priority:",
            item.get(
                "priority_action"
            )
        )

        st.write(
            "Score:",
            item.get(
                "opportunity_score"
            )
        )

        st.write(
            "Probability:",
            item.get(
                "close_probability"
            )
        )

        st.write(
            "Deal Value:",
            item.get(
                "estimated_deal_value"
            )
        )

        st.code(
            item.get(
                "generated_proposal",
                ""
            )
        )

        col1, col2, col3, col4, col5 = (
            st.columns(5)
        )

        with col1:

            if st.button(
                f"Approve {index}"
            ):

                approval_queue.approve(
                    index
                )

                st.rerun()

        with col2:

            if st.button(
                f"Reject {index}"
            ):

                approval_queue.reject(
                    index
                )

                st.rerun()

        with col3:

            if st.button(
                f"Submitted {index}"
            ):

                approval_queue.mark_submitted(
                    index
                )

                st.rerun()

        with col4:

            if st.button(
                f"Won {index}"
            ):

                approval_queue.mark_won(
                    index
                )

                st.rerun()

        with col5:

            if st.button(
                f"Lost {index}"
            ):

                approval_queue.mark_lost(
                    index
                )

                st.rerun()


st.subheader(
    "Learning Intelligence"
)

report = (
    learning_engine.generate_learning_report()
)

st.write(
    "Successful Deals:",
    report.get(
        "wins"
    )
)

st.write(
    "Lost Deals:",
    report.get(
        "losses"
    )
)

st.write(
    "Top Performing Skills:"
)

for skill, score in (
    report.get(
        "top_skills",
        []
    )
):

    st.write(
        f"{skill}: {score}"
    )


st.subheader(
    "Client Relationship Intelligence"
)

client_report = (
    client_memory.generate_report()
)

if client_report:

    client_df = (
        pd.DataFrame(
            client_report
        )
    )

    st.dataframe(
        client_df,
        use_container_width=True
    )

else:

    st.info(
        "No client memory yet."
    )


st.sidebar.success(
    "PhantomOps Runtime Active"
)

st.subheader(
    "Campaign Analytics"
)

campaigns = (
    campaign_engine.load()
)

if campaigns:

    campaign_df = (
        pd.DataFrame(
            campaigns
        )
    )

    st.dataframe(
        campaign_df,
        use_container_width=True
    )

else:

    st.info(
        "No campaigns yet."
    )