"""Adapters for proven external agent systems.

JARVIS remains the authority layer. External projects are execution workers:
- Paperclip: organizational control/task plane.
- Ruflo: swarm/routing/learning execution harness.
- AIReceptionist: optional voice/telephony execution backend.

External projects are invoked as workers; JARVIS owns planning, state and
permission decisions.
"""

from __future__ import annotations

import asyncio
import json
import os
import shlex
import shutil
import urllib.request
import urllib.error
from typing import Any

from .adapters import Worker, WorkerResult


async def _run_command(command: list[str], *, cwd: str | None = None, timeout: int = 900, env: dict[str, str] | None = None) -> WorkerResult:
    try:
        proc = await asyncio.create_subprocess_exec(
            *command,
            cwd=cwd,
            env={**os.environ, **(env or {})},
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return WorkerResult(False, error=f"command timeout after {timeout}s", retryable=True)
        out = stdout.decode(errors="replace").strip()
        err = stderr.decode(errors="replace").strip()
        if proc.returncode != 0:
            return WorkerResult(False, {"stdout": out, "stderr": err}, error=err or out or f"exit {proc.returncode}", retryable=proc.returncode in (124, 137))
        return WorkerResult(True, {"stdout": out, "stderr": err, "exit_code": proc.returncode})
    except FileNotFoundError:
        return WorkerResult(False, error=f"executable not found: {command[0]}")
    except Exception as exc:
        return WorkerResult(False, error=str(exc), retryable=True)


class RufloAdapter(Worker):
    name = "ruflo"
    capabilities = {"swarm", "learning", "multi_agent", "research", "code", "analysis"}

    def score(self, task):
        return 90 if task.get("step", {}).get("capability") in self.capabilities else 0

    async def run(self, task):
        goal = str(task.get("goal") or "")
        context = task.get("context") or {}
        prompt = goal
        if context:
            prompt += "\n\nJARVIS context:\n" + json.dumps(context, ensure_ascii=False, default=str)
        raw = os.getenv("JARVIS_RUFLO_CMD", "npx -y ruflo@latest run")
        command = shlex.split(raw) + [prompt]
        timeout = int(os.getenv("JARVIS_RUFLO_TIMEOUT", "1800"))
        return await _run_command(command, cwd=os.getenv("JARVIS_RUFLO_CWD") or None, timeout=timeout)

    def health(self):
        command = shlex.split(os.getenv("JARVIS_RUFLO_CMD", "npx -y ruflo@latest"))[0]
        return {"ok": bool(shutil.which(command) or command == "npx"), "command": command}


class PaperclipAdapter(Worker):
    name = "paperclip"
    capabilities = {"org_task", "delegation", "business_management", "heartbeat"}

    def score(self, task):
        return 85 if task.get("step", {}).get("capability") in self.capabilities else 0

    async def run(self, task):
        base = os.getenv("JARVIS_PAPERCLIP_URL", "").rstrip("/")
        token = os.getenv("JARVIS_PAPERCLIP_TOKEN", "")
        company = os.getenv("JARVIS_PAPERCLIP_COMPANY_ID", "")
        if not (base and token and company):
            return WorkerResult(False, error="Paperclip not configured; set JARVIS_PAPERCLIP_URL/TOKEN/COMPANY_ID")
        payload = {
            "title": str(task.get("goal") or "JARVIS delegated task"),
            "description": json.dumps({"source": "JARVIS", "context": task.get("context", {}), "step": task.get("step", {})}, ensure_ascii=False, default=str),
        }
        agent_id = os.getenv("JARVIS_PAPERCLIP_AGENT_ID")
        if agent_id:
            payload["assigneeAgentId"] = agent_id
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{base}/api/companies/{company}/issues",
            data=data,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            response = await asyncio.to_thread(urllib.request.urlopen, request, timeout=int(os.getenv("JARVIS_PAPERCLIP_TIMEOUT", "30")))
            body = response.read().decode("utf-8", errors="replace")
            try:
                parsed: Any = json.loads(body)
            except json.JSONDecodeError:
                parsed = {"raw": body}
            return WorkerResult(True, parsed)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            return WorkerResult(False, error=f"Paperclip HTTP {exc.code}: {body}", retryable=exc.code in (429, 502, 503, 504))
        except Exception as exc:
            return WorkerResult(False, error=str(exc), retryable=True)

    def health(self):
        return {"ok": bool(os.getenv("JARVIS_PAPERCLIP_URL") and os.getenv("JARVIS_PAPERCLIP_TOKEN") and os.getenv("JARVIS_PAPERCLIP_COMPANY_ID"))}


class AIReceptionistAdapter(Worker):
    """Optional bridge to a self-hosted AI receptionist project.

    The referenced implementation can handle voice conversations, transfers,
    messages and calendar booking. JARVIS does not copy its code; it invokes a
    local command supplied by the operator. Calls are permission-gated by the
    runtime because the planner marks them as ``external_call``.
    """

    name = "ai_receptionist"
    capabilities = {"voice_receptionist", "appointment_booking", "message_taking", "external_call"}

    def score(self, task):
        return 88 if task.get("step", {}).get("capability") in self.capabilities else 0

    async def run(self, task):
        raw = os.getenv("JARVIS_RECEPTIONIST_CMD", "")
        if not raw:
            return WorkerResult(False, error="AI receptionist not configured; set JARVIS_RECEPTIONIST_CMD")
        goal = str(task.get("goal") or "")
        context = task.get("context") or {}
        payload = json.dumps({"goal": goal, "context": context}, ensure_ascii=False, default=str)
        command = shlex.split(raw) + [payload]
        return await _run_command(
            command,
            cwd=os.getenv("JARVIS_RECEPTIONIST_CWD") or None,
            timeout=int(os.getenv("JARVIS_RECEPTIONIST_TIMEOUT", "900")),
        )

    def health(self):
        raw = os.getenv("JARVIS_RECEPTIONIST_CMD", "")
        if not raw:
            return {"ok": False, "configured": False}
        command = shlex.split(raw)[0]
        return {"ok": bool(shutil.which(command)), "configured": True, "command": command}
