import asyncio
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from .ecosystem_adapters import N8NAdapter, TwentyAdapter


class ErrorHandler(BaseHTTPRequestHandler):
    status_by_path = {
        "/n8n-retry": 503,
        "/n8n-client": 400,
        "/twenty-retry": 429,
        "/twenty-client": 422,
    }

    def do_POST(self):
        status = self.status_by_path[self.path]
        body = f"error-{status}".encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        pass


async def scenario():
    server = ThreadingHTTPServer(("127.0.0.1", 0), ErrorHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    old = {
        key: os.environ.get(key)
        for key in (
            "JARVIS_N8N_WEBHOOK_URL",
            "JARVIS_N8N_WEBHOOK_TOKEN",
            "JARVIS_N8N_TIMEOUT",
            "JARVIS_TWENTY_URL",
            "JARVIS_TWENTY_API_KEY",
            "JARVIS_TWENTY_CRM_PATH",
            "JARVIS_TWENTY_TIMEOUT",
        )
    }
    try:
        os.environ["JARVIS_N8N_WEBHOOK_TOKEN"] = "test-token"
        os.environ["JARVIS_N8N_TIMEOUT"] = "5"
        os.environ["JARVIS_TWENTY_URL"] = base
        os.environ["JARVIS_TWENTY_API_KEY"] = "test-key"
        os.environ["JARVIS_TWENTY_TIMEOUT"] = "5"

        os.environ["JARVIS_N8N_WEBHOOK_URL"] = base + "/n8n-retry"
        n8n = await N8NAdapter().run({"mission_id": "m", "goal": "retry", "step": {}, "context": {}})
        assert not n8n.ok and n8n.retryable
        assert "n8n HTTP 503" in n8n.error
        assert "error-503" in n8n.error

        os.environ["JARVIS_N8N_WEBHOOK_URL"] = base + "/n8n-client"
        n8n_client = await N8NAdapter().run({"mission_id": "m", "goal": "client", "step": {}, "context": {}})
        assert not n8n_client.ok and not n8n_client.retryable
        assert "n8n HTTP 400" in n8n_client.error
        assert "error-400" in n8n_client.error

        os.environ["JARVIS_TWENTY_CRM_PATH"] = "/twenty-retry"
        twenty = await TwentyAdapter().run({"mission_id": "m", "goal": "retry", "step": {}, "context": {"company": "Acme"}})
        assert not twenty.ok and twenty.retryable
        assert "Twenty HTTP 429" in twenty.error
        assert "error-429" in twenty.error

        os.environ["JARVIS_TWENTY_CRM_PATH"] = "/twenty-client"
        twenty_client = await TwentyAdapter().run({"mission_id": "m", "goal": "client", "step": {}, "context": {"company": "Acme"}})
        assert not twenty_client.ok and not twenty_client.retryable
        assert "Twenty HTTP 422" in twenty_client.error
        assert "error-422" in twenty_client.error
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
    print("JARVIS-NEXT HTTP ADAPTER ERROR CONTRACT OK")


if __name__ == "__main__":
    main()
