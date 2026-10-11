# JARVIS-NEXT integration map

## Adopted external capabilities

- OpenClaw: persistent local assistant/gateway, channels, skills and device-facing execution. Use as a worker, never as JARVIS authority.
- Browser Use: browser-agent worker for complex navigation; keep approval gates around external sends, purchases and submissions.
- OpenHands: coding/software-engineering worker for repository changes and test loops.
- Ruflo: swarm/multi-agent/learning execution worker when a task benefits from a parallel agent harness.
- Paperclip: organizational task/delegation worker; JARVIS remains the executive authority.
- AI receptionist backend: optional voice/telephony worker for inbound calls, appointment booking and message taking.
- n8n: workflow/integration worker for CRM, email, messaging, databases and other connected systems.
- Twenty: optional open-source CRM backend for structured lead/company synchronization through its workspace REST API. Twenty is a worker, not an authority layer.

## Existing capability retained

PhantomOps remains the revenue worker: leads, research, scoring, CRM, proposals, outreach, follow-up, marketplace and analytics.

## Selection principle

Prefer native existing PhantomOps tools when sufficient. Escalate to external workers only when they add a concrete missing capability. All workers report results back to JARVIS-NEXT state and permissions.

## CRM routing

For CRM/workflow missions, JARVIS first plans the workflow and checks permission. If Twenty is configured, its higher worker score makes it the preferred `crm_sync`/`integration` backend; otherwise n8n can execute the integration through its webhook. External CRM writes remain approval-gated.

### Twenty configuration

Set these environment variables when using a self-hosted or cloud Twenty workspace:

- `JARVIS_TWENTY_URL` — Twenty base URL.
- `JARVIS_TWENTY_API_KEY` — Twenty API key.
- `JARVIS_TWENTY_CRM_PATH` — REST path, default `/rest/companies`.
- `JARVIS_TWENTY_METHOD` — HTTP method, default `POST`.
- `JARVIS_TWENTY_TIMEOUT` — request timeout in seconds, default `30`.

Twenty's API is workspace-specific and supports REST and GraphQL; keep the REST path configurable rather than hard-coding a schema that may differ between workspaces.
