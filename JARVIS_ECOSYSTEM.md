# JARVIS Ecosystem Stack

JARVIS-NEXT is the authority and durable mission runtime. It does not replace the mature systems already built in NEXUS/PhantomOps; it coordinates them.

## Integrated roles

| Layer | System | Role |
|---|---|---|
| Executive authority | JARVIS-NEXT | mission state, planning, permissions, approvals, resume, verification |
| Organizational control plane | Paperclip | companies, org chart, goals, delegated tasks, heartbeats, audit and budgets |
| Runtime/supervision | NEXUS / GRAM / GOVI | existing stable execution and domain agents |
| Revenue execution | PhantomOps | leads, opportunities, proposals, delivery, CRM, follow-up |
| Swarm/learning | Ruflo | multi-agent execution, routing, learning and memory harness |
| Browser execution | BrowserWorker / Browser Use | browser research and computer interaction |
| Software execution | OpenHands | coding, repository work, tests and maintenance |
| Persistent state | JARVIS SQLite | missions, events, approvals and resumable context |

## Authority rule

Only JARVIS decides whether a mission step may execute. External systems are workers/control-plane integrations. They must not become competing executive authorities.

Sensitive actions (`external_send`, payment, purchase, delete, legal commitment, credential changes) remain approval-gated.

## Optional integrations

### Ruflo

Set:

```text
JARVIS_RUFLO_CMD=npx -y ruflo@latest run
JARVIS_RUFLO_TIMEOUT=1800
JARVIS_RUFLO_CWD=<project directory>
```

The adapter invokes Ruflo only when the planner selects `swarm`, `learning`, `multi_agent`, `analysis`, or related capabilities. Ruflo can also be installed locally and exposed through a different command by changing `JARVIS_RUFLO_CMD`.

### Paperclip

Set:

```text
JARVIS_PAPERCLIP_URL=http://127.0.0.1:3100
JARVIS_PAPERCLIP_TOKEN=<token>
JARVIS_PAPERCLIP_COMPANY_ID=<company-id>
JARVIS_PAPERCLIP_AGENT_ID=<optional-agent-id>
JARVIS_PAPERCLIP_TIMEOUT=30
```

JARVIS delegates an organizational task to Paperclip through its company issue API. Paperclip then manages the organizational work/agent lifecycle while JARVIS retains mission authority.

## Execution examples

- `find qualified healthcare prospects` → JARVIS → PhantomOps/NEXUS → approval → outreach.
- `run a swarm research task` → JARVIS → Ruflo.
- `delegate this research to the agent team` → JARVIS → Paperclip.
- `build and test this feature` → JARVIS → OpenHands.
- `research this website` → JARVIS → browser worker.

## Principle

**Integrate first, replace last.** Existing NEXUS, GRAM, GOVI and PhantomOps work stays in place. Proven open-source systems supply missing execution/orchestration capabilities through adapters.
