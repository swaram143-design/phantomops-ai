"""Adapters for proven external agent systems.

JARVIS remains the authority layer. External projects are execution workers:
- Paperclip: organizational control/task plane.
- Ruflo: swarm/routing/learning execution harness.
- AIReceptionist: optional voice/telephony execution backend.
- n8n: workflow/integration execution backend.
- Twenty: optional open-source CRM execution backend.

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


def _idempotency_key(task: dict[str, Any]) -> str | None:
    """Return the runtime execution identity supplied to an external worker."""
    value = task.get("idempotency_key")
    return str(value) if value is not None else None


def _idempotency_headers(task: dict[str, Any]) -> dict[str, str]:
    """Expose the execution identity through the standard HTTP idempotency header."""
    key = _idempotency_key(task)
    return {"Idempotency-Key": key} if key else {}


def _ambiguous_timeout(exc: BaseException, adapter: str) -> WorkerResult:
    """A request timeout has unknown remote outcome; never blindly retry it."""
    return WorkerResult(False, error=f"{adapter} request outcome unknown after timeout: {exc}", retryable=False)


def _is_timeout_error(exc: BaseException) -> bool:
    """Recognize direct and urllib-wrapped socket timeouts."""
    if isinstance(exc, TimeoutError):
        return True
    return isinstance(exc, urllib.error.URLError) and isinstance(exc.reason, TimeoutError)


async def _run_command(command: list[str], *, cwd: str | None = None, timeout: int = 900, env: dict[str, str] | None = None) -> WorkerResult:
    try:
        proc = await asyncio.create_subprocess_exec(*command, cwd=cwd, env={**os.environ, **(env or {})}, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill(); await proc.wait()
            return WorkerResult(False, error=f"command timeout after {timeout}s", retryable=True)
        out = stdout.decode(errors="replace").strip(); err = stderr.decode(errors="replace").strip()
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
        prompt = str(task.get("goal") or "")
        if task.get("context"):
            prompt += "\n\nJARVIS context:\n" + json.dumps(task["context"], ensure_ascii=False, default=str)
        key = _idempotency_key(task)
        if key: prompt += "\n\nJARVIS idempotency key:\n" + key
        command = shlex.split(os.getenv("JARVIS_RUFLO_CMD", "npx -y ruflo@latest run")) + [prompt]
        env = {"JARVIS_IDEMPOTENCY_KEY": key} if key else None
        return await _run_command(command, cwd=os.getenv("JARVIS_RUFLO_CWD") or None, timeout=int(os.getenv("JARVIS_RUFLO_TIMEOUT", "1800")), env=env)
    def health(self):
        command = shlex.split(os.getenv("JARVIS_RUFLO_CMD", "npx -y ruflo@latest"))[0]
        return {"ok": bool(shutil.which(command) or command == "npx"), "command": command}


class PaperclipAdapter(Worker):
    name = "paperclip"
    capabilities = {"org_task", "delegation", "business_management", "heartbeat"}
    def score(self, task):
        return 85 if task.get("step", {}).get("capability") in self.capabilities else 0
    async def run(self, task):
        base = os.getenv("JARVIS_PAPERCLIP_URL", "").rstrip("/"); token = os.getenv("JARVIS_PAPERCLIP_TOKEN", ""); company = os.getenv("JARVIS_PAPERCLIP_COMPANY_ID", "")
        if not (base and token and company): return WorkerResult(False, error="Paperclip not configured; set JARVIS_PAPERCLIP_URL/TOKEN/COMPANY_ID")
        key = _idempotency_key(task)
        description = {"source":"JARVIS","context":task.get("context",{}),"step":task.get("step",{})}
        if key: description["idempotency_key"] = key
        payload = {"title": str(task.get("goal") or "JARVIS delegated task"), "description": json.dumps(description, ensure_ascii=False, default=str)}
        if os.getenv("JARVIS_PAPERCLIP_AGENT_ID"): payload["assigneeAgentId"] = os.getenv("JARVIS_PAPERCLIP_AGENT_ID")
        headers = {"Authorization":f"Bearer {token}","Content-Type":"application/json",**_idempotency_headers(task)}
        request = urllib.request.Request(f"{base}/api/companies/{company}/issues", data=json.dumps(payload).encode(), headers=headers, method="POST")
        try:
            response = await asyncio.to_thread(urllib.request.urlopen, request, timeout=int(os.getenv("JARVIS_PAPERCLIP_TIMEOUT", "30"))); body = response.read().decode("utf-8", errors="replace")
            try: parsed: Any = json.loads(body)
            except json.JSONDecodeError: parsed = {"raw": body}
            return WorkerResult(True, parsed)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace"); return WorkerResult(False, error=f"Paperclip HTTP {exc.code}: {body}", retryable=exc.code in (429,502,503,504))
        except Exception as exc:
            if _is_timeout_error(exc): return _ambiguous_timeout(exc, "Paperclip")
            return WorkerResult(False, error=str(exc), retryable=True)
    def health(self): return {"ok": bool(os.getenv("JARVIS_PAPERCLIP_URL") and os.getenv("JARVIS_PAPERCLIP_TOKEN") and os.getenv("JARVIS_PAPERCLIP_COMPANY_ID"))}


class AIReceptionistAdapter(Worker):
    name = "ai_receptionist"
    capabilities = {"voice_receptionist", "appointment_booking", "message_taking", "external_call"}
    def score(self, task): return 88 if task.get("step", {}).get("capability") in self.capabilities else 0
    async def run(self, task):
        raw = os.getenv("JARVIS_RECEPTIONIST_CMD", "")
        if not raw: return WorkerResult(False, error="AI receptionist not configured; set JARVIS_RECEPTIONIST_CMD")
        payload = json.dumps({"goal":str(task.get("goal") or ""),"context":task.get("context",{}),"idempotency_key":_idempotency_key(task)}, ensure_ascii=False, default=str)
        key = _idempotency_key(task); env = {"JARVIS_IDEMPOTENCY_KEY": key} if key else None
        return await _run_command(shlex.split(raw) + [payload], cwd=os.getenv("JARVIS_RECEPTIONIST_CWD") or None, timeout=int(os.getenv("JARVIS_RECEPTIONIST_TIMEOUT", "900")), env=env)
    def health(self):
        raw = os.getenv("JARVIS_RECEPTIONIST_CMD", "")
        if not raw: return {"ok":False,"configured":False}
        command = shlex.split(raw)[0]; return {"ok":bool(shutil.which(command)),"configured":True,"command":command}


class N8NAdapter(Worker):
    name = "n8n"
    capabilities = {"workflow_automation", "crm_sync", "integration", "followup_automation"}
    def score(self, task): return 86 if task.get("step", {}).get("capability") in self.capabilities else 0
    async def run(self, task):
        url = os.getenv("JARVIS_N8N_WEBHOOK_URL", "")
        if not url: return WorkerResult(False, error="n8n not configured; set JARVIS_N8N_WEBHOOK_URL")
        payload = {"source":"JARVIS","mission_id":task.get("mission_id"),"goal":task.get("goal"),"step":task.get("step",{}),"context":task.get("context",{}),"idempotency_key":_idempotency_key(task)}
        headers = {"Content-Type":"application/json", **_idempotency_headers(task)}; token = os.getenv("JARVIS_N8N_WEBHOOK_TOKEN", "")
        if token: headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, data=json.dumps(payload, ensure_ascii=False, default=str).encode(), headers=headers, method="POST")
        try:
            response = await asyncio.to_thread(urllib.request.urlopen, request, timeout=int(float(os.getenv("JARVIS_N8N_TIMEOUT", "60")))); body = response.read().decode("utf-8", errors="replace")
            try: parsed: Any = json.loads(body)
            except json.JSONDecodeError: parsed = {"raw": body}
            return WorkerResult(True, parsed)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace"); return WorkerResult(False, error=f"n8n HTTP {exc.code}: {body}", retryable=exc.code in (429,502,503,504))
        except Exception as exc:
            if _is_timeout_error(exc): return _ambiguous_timeout(exc, "n8n")
            return WorkerResult(False, error=str(exc), retryable=True)
    def health(self): return {"ok": bool(os.getenv("JARVIS_N8N_WEBHOOK_URL")), "configured": bool(os.getenv("JARVIS_N8N_WEBHOOK_URL"))}


class TwentyAdapter(Worker):
    """Optional Twenty CRM backend."""
    name = "twenty"
    capabilities = {"crm_sync", "integration"}
    def score(self, task): return 92 if task.get("step", {}).get("capability") in self.capabilities else 0
    async def run(self, task):
        base = os.getenv("JARVIS_TWENTY_URL", "").rstrip("/"); token = os.getenv("JARVIS_TWENTY_API_KEY", ""); path = os.getenv("JARVIS_TWENTY_CRM_PATH", "/rest/companies")
        if not (base and token): return WorkerResult(False, error="Twenty not configured; set JARVIS_TWENTY_URL/JARVIS_TWENTY_API_KEY")
        context = task.get("context", {}) or {}; target = context.get("selected_target") or {}
        payload = {"name": context.get("company") or target.get("company") or "JARVIS lead", "email": context.get("recipient") or target.get("email"), "source": "JARVIS", "goal": task.get("goal"), "need": context.get("need") or target.get("need"), "score": context.get("selection_score") or target.get("score"), "idempotency_key": _idempotency_key(task)}
        payload = {k: v for k, v in payload.items() if v is not None}
        request = urllib.request.Request(f"{base}{path}", data=json.dumps(payload, ensure_ascii=False, default=str).encode(), headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", **_idempotency_headers(task)}, method=os.getenv("JARVIS_TWENTY_METHOD", "POST").upper())
        try:
            response = await asyncio.to_thread(urllib.request.urlopen, request, timeout=int(float(os.getenv("JARVIS_TWENTY_TIMEOUT", "30")))); body = response.read().decode("utf-8", errors="replace")
            try: parsed: Any = json.loads(body)
            except json.JSONDecodeError: parsed = {"raw": body}
            return WorkerResult(True, parsed)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace"); return WorkerResult(False, error=f"Twenty HTTP {exc.code}: {body}", retryable=exc.code in (429,502,503,504))
        except Exception as exc:
            if _is_timeout_error(exc): return _ambiguous_timeout(exc, "Twenty")
            return WorkerResult(False, error=str(exc), retryable=True)
    def health(self):
        configured = bool(os.getenv("JARVIS_TWENTY_URL") and os.getenv("JARVIS_TWENTY_API_KEY")); return {"ok": configured, "configured": configured, "base_url": bool(os.getenv("JARVIS_TWENTY_URL")), "api_key": bool(os.getenv("JARVIS_TWENTY_API_KEY"))}
