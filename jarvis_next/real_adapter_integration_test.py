import asyncio
import json
import os
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from .adapters import Worker, WorkerRegistry, WorkerResult
from .ecosystem_adapters import N8NAdapter, TwentyAdapter
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


class WebhookHandler(BaseHTTPRequestHandler):
    calls = []

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        payload = json.loads(body.decode("utf-8"))
        self.__class__.calls.append(
            {
                "path": self.path,
                "payload": payload,
                "auth": self.headers.get("Authorization"),
            }
        )
        response = {
            "success": True,
            "id": "crm-acme-001" if self.path == "/twenty/rest/companies" else "workflow-001",
        }
        encoded = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *_args):
        pass


class SendWorker(Worker):
    name = "send_test_worker"
    capabilities = {"external_send"}

    async def run(self, task):
        return WorkerResult(True, {"sent": True, "recipient": task["context"]["recipient"]})


async def scenario():
    WebhookHandler.calls = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), WebhookHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    old = {
        k: os.environ.get(k)
        for k in (
            "JARVIS_N8N_WEBHOOK_URL",
            "JARVIS_N8N_WEBHOOK_TOKEN",
            "JARVIS_TWENTY_URL",
            "JARVIS_TWENTY_API_KEY",
            "JARVIS_TWENTY_CRM_PATH",
        )
    }
    os.environ["JARVIS_N8N_WEBHOOK_URL"] = base + "/n8n"
    os.environ["JARVIS_N8N_WEBHOOK_TOKEN"] = "test-token"
    os.environ["JARVIS_TWENTY_URL"] = base
    os.environ["JARVIS_TWENTY_API_KEY"] = "test-key"
    os.environ["JARVIS_TWENTY_CRM_PATH"] = "/twenty/rest/companies"
    try:
        twenty = TwentyAdapter()
        n8n = N8NAdapter()
        direct = await twenty.run(
            {
                "goal": "sync Acme Clinic",
                "mission_id": "m-direct",
                "step": {"capability": "crm_sync", "action": "workflow_trigger"},
                "context": {
                    "company": "Acme Clinic",
                    "recipient": "owner@acme.example",
                    "need": "appointment recovery",
                    "selection_score": 91,
                },
            }
        )
        assert direct.ok and direct.data["id"] == "crm-acme-001"
        assert WebhookHandler.calls[-1]["auth"] == "Bearer test-key"

        workflow = await n8n.run(
            {
                "goal": "schedule follow-up",
                "mission_id": "m-direct",
                "step": {"capability": "followup_automation", "action": "workflow_trigger"},
                "context": {"company": "Acme Clinic", "crm_id": "crm-acme-001", "sent": True},
            }
        )
        assert workflow.ok and workflow.data["id"] == "workflow-001"
        assert WebhookHandler.calls[-1]["auth"] == "Bearer test-token"
        assert WebhookHandler.calls[0]["payload"]["context"]["company"] == "Acme Clinic"
        assert WebhookHandler.calls[1]["payload"]["context"]["crm_id"] == "crm-acme-001"
        assert WebhookHandler.calls[1]["payload"]["context"]["sent"] is True

        with tempfile.TemporaryDirectory() as tmp:
            db = f"{tmp}/jarvis.db"
            state = StateStore(db)
            registry = WorkerRegistry()
            registry.register(twenty)
            registry.register(SendWorker())
            registry.register(n8n)
            runtime = JarvisRuntime(
                state=state,
                workers=registry,
                permissions=PermissionEngine("WORK"),
                max_retries=0,
            )
            plan = {
                "goal": "real adapter revenue test",
                "steps": [
                    {"capability": "crm_sync", "action": "workflow_trigger"},
                    {"capability": "external_send", "action": "external_send"},
                    {"capability": "followup_automation", "action": "workflow_trigger"},
                ],
            }
            runtime.planner.plan = lambda goal, context: plan
            before_runtime_calls = len(WebhookHandler.calls)
            first = await runtime.submit(
                "real adapter revenue test",
                {
                    "company": "Acme Clinic",
                    "recipient": "owner@acme.example",
                    "need": "appointment recovery",
                    "selection_score": 91,
                },
            )
            assert first["status"] == "awaiting_approval" and first["step_index"] == 0
            assert len(WebhookHandler.calls) == before_runtime_calls, (
                "CRM side effect must not happen before approval"
            )

            approval = first["approval_id"]
            restarted = JarvisRuntime(
                state=StateStore(db),
                workers=registry,
                permissions=PermissionEngine("WORK"),
                max_retries=0,
            )
            resumed = await restarted.resume_mission(first["mission_id"])
            assert resumed["status"] == "awaiting_approval" and resumed["approval_id"] == approval

            after_crm = await restarted.resume(approval, approved=True)
            assert after_crm["status"] == "awaiting_approval" and after_crm["step_index"] == 1
            assert after_crm["context"].get("id") == "crm-acme-001"
            assert after_crm["context"]["company"] == "Acme Clinic"

            send_approval = after_crm["approval_id"]
            after_send = await restarted.resume(send_approval, approved=True)
            assert after_send["status"] == "awaiting_approval" and after_send["step_index"] == 2
            assert after_send["context"]["sent"] is True

            final = await restarted.resume(after_send["approval_id"], approved=True)
            assert final["status"] == "completed"
            assert any(c["path"] == "/twenty/rest/companies" for c in WebhookHandler.calls)
            assert any(
                c["path"] == "/n8n" and c["payload"]["context"].get("crm_id")
                for c in WebhookHandler.calls
            )
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        server.shutdown()
        server.server_close()


def main():
    asyncio.run(scenario())
    print("JARVIS-NEXT REAL ADAPTER INTEGRATION OK")


if __name__ == "__main__":
    main()
