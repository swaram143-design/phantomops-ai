# PhantomOps Healthcare Revenue Desk — pilot MVP

## Commercial offer
A managed enquiry-handling and follow-up workflow for independent clinics and diagnostic centres.

Suggested validation offer (not a proven market price):
- 14-day paid pilot: ₹9,999
- Managed service after a successful pilot: test ₹14,999–₹24,999/month
- Sell the operational outcome: enquiry visibility, assigned follow-ups and weekly conversion reporting.

## Current implementation
This branch adds a single-customer pilot API:
- API-key protected enquiry create/list/update endpoints.
- SQLite persistence.
- Status counts and due-follow-up count.
- Minimal operational fields only.

Run locally:
```bash
set PHANTOMOPS_API_KEY=replace-with-a-long-random-secret
set PHANTOMOPS_HEALTHCARE_DB=data/healthcare_revenue.db
uvicorn healthcare_revenue_api:app --host 127.0.0.1 --port 8010
```

Send `X-API-Key: <your key>` with every `/api/*` request. `/health` is public.
Swagger docs are available at `/docs` on the local server.

## Local operator dashboard

Open a second Windows Command Prompt from the repository root. Set the same API key used by the API process, then run:

```bat
set PHANTOMOPS_API_KEY=your-local-secret
set PHANTOMOPS_API_URL=http://127.0.0.1:8010
streamlit run healthcare_revenue_app.py
```

The dashboard is intended for a trusted local operator on the same machine/network. Do not expose Streamlit or the API directly to the public internet without adding production authentication, HTTPS, access controls and deployment hardening.

Example create:
```json
{
  "contact_name": "Demo Contact",
  "contact_phone": "+910000000000",
  "service_category": "General consultation",
  "source": "website",
  "next_followup_at": "2026-11-10T10:00:00+05:30"
}
```

## Important limits before a live clinic deployment
- This is a single-tenant pilot API, not a multi-tenant SaaS product.
- Deploy a separate isolated instance and database for each pilot customer.
- Use synthetic data for demos. For real enquiries, obtain the clinic's documented authorisation and establish lawful notice/consent, access controls, encryption, backup, retention and deletion procedures.
- Do not enter diagnoses, medical notes, prescriptions, test results, medical-record identifiers or other clinical content.
- Do not send automated patient messages until approved templates, consent/opt-out handling, delivery logs and clinic review are implemented.
- No billing/subscription system, production hosting, monitoring, customer onboarding UI or live integrations are included yet.
- Pilot price and monthly pricing are hypotheses to validate with customers, not guaranteed sales.

## Security remediation
The SMTP sender now reads credentials from `SMTP_EMAIL` and `SMTP_PASSWORD`; it no longer contains a committed password. This does not revoke any previously exposed credential. Revoke the old Gmail app password in the Google account and create a new one only after the code is deployed securely.
