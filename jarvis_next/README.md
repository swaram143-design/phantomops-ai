# JARVIS-NEXT

Additive executive runtime for the existing PhantomOps/JARVIS codebase.

JARVIS owns mission planning, durable state, permissions, approvals, retries, leases, and resume. Execution systems remain replaceable workers; JARVIS does not delegate authority over mission state or approval decisions to them.

## Current worker integrations

The runtime registry currently includes these execution workers:

- **PhantomOps** — revenue and CRM execution, including the local CRM-memory path.
- **Browser** — browser execution worker.
- **OpenClaw** — external execution worker.
- **OpenHands** — external execution worker.
- **Ruflo** — swarm/research/code/analysis execution worker.
- **Paperclip** — organizational task/delegation worker when configured.
- **AI Receptionist** — voice/reception/appointment execution worker when configured.
- **n8n** — webhook-based workflow/integration worker when configured.
- **Twenty** — optional CRM HTTP worker when configured.
- **NEXUS legacy** — optional compatibility worker when `NEXUS_ROOT` is configured.

Worker selection is capability-based and scored by the registry. The runtime supplies an execution-specific idempotency key to workers so external adapters can propagate the same mission/step identity.

## Durability and safety

The runtime persists mission progress and step outputs, supports approval gates, retries, worker fallback, mission leases, restart/resume, blocked/failed states, and approval deduplication. High-risk actions are not executed until the required approval is resolved.

Runtime context is treated as data rather than as authority: the current step, mission identity, and other runtime control fields are written after persisted worker context so stale worker output cannot overwrite the step being dispatched.

## Verification

The `jarvis-next` smoke workflow runs the contract suite on pushes and pull requests affecting `jarvis_next` or the workflow itself. The suite covers runtime durability, approval/rejection behavior, retries, fallback, leases, restart/resume, planner failure handling, revenue flow, and local HTTP integration contracts for Twenty and n8n.

The Twenty/n8n integration tests use local test HTTP servers to verify request shape, authorization, idempotency propagation, approval gating, restart/resume, and final mission completion. They do **not** claim that a live third-party Twenty or n8n deployment is configured or that an external production side effect has occurred.

## Operational boundary

A green CI run proves the checked-in contracts and local integration behavior for the tested configuration. It is not, by itself, proof of production deployment, live third-party credentials, real customer outreach, or revenue.
