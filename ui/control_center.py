import streamlit as st
import pandas as pd
import os
import psutil
import time

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="PhantomOps Control Center",

    page_icon="🚀",

    layout="wide",

    initial_sidebar_state="collapsed"
)

# =====================================================
# HIDE STREAMLIT UI
# =====================================================

hide_streamlit_style = """

<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

[data-testid="collapsedControl"] {
    display: none;
}

</style>

"""

st.markdown(
    hide_streamlit_style,
    unsafe_allow_html=True
)

# =====================================================
# TITLE
# =====================================================

st.title(
    "🚀 PHANTOMOPS CONTROL CENTER"
)

st.markdown(
    "### Autonomous AI Operations Platform"
)

# =====================================================
# SYSTEM STATUS
# =====================================================

st.subheader("SYSTEM STATUS")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Agents",
    "6 ACTIVE"
)

col2.metric(
    "Autonomous Loop",
    "RUNNING"
)

col3.metric(
    "Task Queue",
    "MONITORING"
)

# =====================================================
# SYSTEM RESOURCE MONITOR
# =====================================================

st.subheader("SYSTEM RESOURCE MONITOR")

cpu_usage = psutil.cpu_percent()

ram_usage = psutil.virtual_memory().percent

disk_usage = psutil.disk_usage('/').percent

r1, r2, r3 = st.columns(3)

r1.metric(
    "CPU Usage",
    f"{cpu_usage}%"
)

r2.metric(
    "RAM Usage",
    f"{ram_usage}%"
)

r3.metric(
    "Disk Usage",
    f"{disk_usage}%"
)

# =====================================================
# LOAD CSV
# =====================================================

def load_csv(path):

    if os.path.exists(path):

        return pd.read_csv(path)

    return None

# =====================================================
# LEAD DATABASE
# =====================================================

st.subheader("LEAD DATABASE")

leads = load_csv(
    "database/scored_leads.csv"
)

if leads is not None:

    st.dataframe(
        leads,
        use_container_width=True
    )

else:

    st.warning(
        "No lead database found."
    )

# =====================================================
# CAMPAIGNS
# =====================================================

st.subheader("CAMPAIGN TRACKER")

campaigns = load_csv(
    "database/campaigns.csv"
)

if campaigns is not None:

    st.dataframe(
        campaigns,
        use_container_width=True
    )

else:

    st.warning(
        "No campaign database found."
    )

# =====================================================
# CONTACTS
# =====================================================

st.subheader("CONTACT DISCOVERY")

contacts = load_csv(
    "database/contacts.csv"
)

if contacts is not None:

    st.dataframe(
        contacts,
        use_container_width=True
    )

else:

    st.warning(
        "No contacts database found."
    )

# =====================================================
# LIVE OPERATIONS
# =====================================================

st.subheader("LIVE OPERATIONS")

st.success(
    "Autonomous loop operational."
)

st.info(
    "Agents are monitoring workflows."
)

st.info(
    "Campaign tracking active."
)

st.info(
    "Lead intelligence engine active."
)

# =====================================================
# LIVE ACTIVITY FEED
# =====================================================

st.subheader("LIVE ACTIVITY FEED")

log_file = "database/activity_log.txt"

if os.path.exists(log_file):

    with open(
        log_file,
        "r",
        encoding="utf-8"
    ) as file:

        logs = file.readlines()

    logs = logs[-20:]

    activity_text = ""

    for log in logs:

        activity_text += log

    st.text_area(

        "Operations Log",

        activity_text,

        height=300
    )

else:

    st.warning(
        "No activity logs found."
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "PhantomOps Autonomous AI Infrastructure"
)