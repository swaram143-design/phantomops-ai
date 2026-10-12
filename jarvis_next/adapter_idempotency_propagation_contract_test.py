import asyncio
import json
import os
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from .ecosystem_adapters import N8NAdapter, TwentyAdapter


class Handler(BaseHTTPRequestHandler):
    payloads = []

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        self.__class__.payloads.append(json.loads(body.decode("utf-8")))
        response = json.dumps({"ok": True}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, *_args):
        pass


async def scenario():
    Handler.payloads = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    old = {k: os.environ.get(k) for k in ("JARVIS_N8N_WEBHOOK_URL", "JARVIS_N8N_WEBHOOK_TOKEN", "JARVIS_TWENTY_URL", "JARVIS_TWENTY_API_KEY", "JARVIS_TWENTY_CRM_PATH")}
    os.environ["JARVIS_N8N_WEBHOOK_URL"] = base + "/n8n"
    os.environ["JARVIS_N8N_WEBHOOK_TOKEN"] = "test-token"
    os.environ["JARVIS_TWENTY_URL"] = base
    os.environ["JARVIS_TWENTY_API_KEY"] = "test-key"
    os.environ["JARVIS_TWENTY_CRM_PATH"] = "/twenty/rest/companies"
    key = "mission-123:0:twenty"
    try:
        twenty = TwentyAdapter()
        result = await twenty.run({
            "mission_id": "mission-123",
            "idempotency_key": key,
            "goal": "sync Acme Clinic",
            "step": {"capability": "crm_sync", "action": "workflow_trigger"},
            "context": {"company": "Acme Clinic", "recipient": "owner@acme.example"},
        })
        assert result.ok
        assert Handler.payloads[-1]["idempotency_key"] == key

        n8n = N8NAdapter()
        n8n_key = "mission-123:1:n8n"
        result = await n8n.run({
            "mission_id": "mission-123",
            "idempotency_key": n8n_key,
            "goal": "schedule follow-up",
            "step": {"capability": "followup_automation", "action": "workflow_trigger"},
            "context": {"company": "Acme Clinic"},
        })
        assert result.ok
        assert Handler.payloads[-1]["idempotency_key"] == n8n_key
    finally:
        for key_name, value in old.items():
            if value is None:
                os.environ.pop(key_name, None)
            else:
                os.environ[key_name] = value
        server.shutdown()
        server.server_close()


def main():
    asyncio.run(scenario())
    print("JARVIS-NEXT ADAPTER IDEMPOTENCY PROPAGATION CONTRACT OK")


if __name__ == "__main__":
    main()
