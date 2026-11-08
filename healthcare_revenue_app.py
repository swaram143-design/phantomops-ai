"""Local operator dashboard for the single-tenant healthcare revenue pilot."""
import os
from datetime import datetime, date, time

import requests
import streamlit as st


st.set_page_config(
    page_title="PhantomOps Healthcare Revenue Desk",
    page_icon="📈",
    layout="wide",
)

API_BASE = os.getenv("PHANTOMOPS_API_URL", "http://127.0.0.1:8010").rstrip("/")
API_KEY = os.getenv("PHANTOMOPS_API_KEY", "").strip()
HEADERS = {"X-API-Key": API_KEY}


def api_request(method, path, **kwargs):
    response = requests.request(
        method,
        f"{API_BASE}{path}",
        headers=HEADERS,
        timeout=10,
        **kwargs,
    )
    response.raise_for_status()
    return response.json()


st.title("PhantomOps Healthcare Revenue Desk")
st.caption("Enquiry visibility · follow-up control · appointment workflow")

if not API_KEY:
    st.error("Dashboard API key is not configured.")
    st.code("set PHANTOMOPS_API_KEY=your-local-secret")
    st.info("Use the same local API key that was configured when starting the API server.")
    st.stop()

try:
    health = requests.get(f"{API_BASE}/health", timeout=5)
    health.raise_for_status()
except requests.RequestException:
    st.error("The revenue API is not reachable. Start healthcare_revenue_api.py first.")
    st.code("uvicorn healthcare_revenue_api:app --host 127.0.0.1 --port 8010")
    st.stop()

try:
    metrics = api_request("GET", "/api/metrics")
    listing = api_request("GET", "/api/enquiries", params={"limit": 500})
except requests.RequestException as error:
    st.error(f"Could not load enquiry data: {error}")
    st.stop()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total enquiries", metrics.get("total_enquiries", 0))
m2.metric("New", metrics.get("by_status", {}).get("new", 0))
m3.metric("Appointments booked", metrics.get("by_status", {}).get("appointment_booked", 0))
m4.metric("Follow-ups due", metrics.get("followups_due", 0))

st.divider()
left, right = st.columns([1, 1])

with left:
    st.subheader("Capture an enquiry")
    with st.form("new_enquiry", clear_on_submit=True):
        contact_name = st.text_input("Contact name")
        contact_phone = st.text_input("Contact phone")
        service_category = st.text_input("Service category", placeholder="e.g. General consultation")
        source = st.selectbox("Enquiry source", ["staff_entry", "website", "phone", "walk_in", "referral"])
        schedule_followup = st.checkbox("Schedule a follow-up")
        followup_date = st.date_input("Follow-up date", value=date.today()) if schedule_followup else None
        followup_time = st.time_input("Follow-up time", value=time(10, 0)) if schedule_followup else None
        submitted = st.form_submit_button("Save enquiry", type="primary")

        if submitted:
            if not contact_name.strip() or not contact_phone.strip() or not service_category.strip():
                st.error("Enter the contact name, phone and service category.")
            else:
                payload = {
                    "contact_name": contact_name.strip(),
                    "contact_phone": contact_phone.strip(),
                    "service_category": service_category.strip(),
                    "source": source,
                }
                if schedule_followup and followup_date and followup_time:
                    local_dt = datetime.combine(followup_date, followup_time).astimezone()
                    payload["next_followup_at"] = local_dt.isoformat()
                try:
                    created = api_request("POST", "/api/enquiries", json=payload)
                    st.success(f"Enquiry saved: {created['id']}")
                    st.rerun()
                except requests.RequestException as error:
                    st.error(f"Could not save enquiry: {error}")

with right:
    st.subheader("Update enquiry status")
    enquiries = listing.get("enquiries", [])
    if enquiries:
        choices = {
            f"{item['contact_name']} · {item['service_category']} · {item['id'][:8]}": item["id"]
            for item in enquiries
        }
        with st.form("update_enquiry"):
            selected_label = st.selectbox("Select enquiry", list(choices.keys()))
            new_status = st.selectbox(
                "New status",
                ["new", "contacted", "appointment_booked", "completed", "closed"],
            )
            update_submitted = st.form_submit_button("Update status")
            if update_submitted:
                try:
                    api_request(
                        "PATCH",
                        f"/api/enquiries/{choices[selected_label]}",
                        json={"status": new_status},
                    )
                    st.success("Enquiry status updated.")
                    st.rerun()
                except requests.RequestException as error:
                    st.error(f"Could not update enquiry: {error}")
    else:
        st.info("No enquiries yet. Add a demonstration enquiry to begin.")

st.divider()
st.subheader("Enquiry pipeline")
if listing.get("enquiries"):
    display_rows = [
        {
            "Contact": item["contact_name"],
            "Phone": item["contact_phone"],
            "Service": item["service_category"],
            "Source": item["source"],
            "Status": item["status"],
            "Next follow-up": item["next_followup_at"] or "Not scheduled",
            "Created": item["created_at"],
        }
        for item in listing["enquiries"]
    ]
    st.dataframe(display_rows, use_container_width=True, hide_index=True)
else:
    st.info("The pipeline is empty.")

st.caption(
    "Pilot safety: use synthetic data for demonstrations. Do not enter diagnoses, "
    "clinical notes, prescriptions, reports or medical-record content. "
    "Use real contact information only after the clinic has authorised the workflow "
    "and approved the required privacy and retention controls."
)
