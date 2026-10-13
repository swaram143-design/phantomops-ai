import asyncio
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .ecosystem_adapters import N8NAdapter, TwentyAdapter


class SlowAcceptedHandler(BaseHTTPRequestHandler):
    calls = 0

    def do_POST(self):
        type(self).calls += 1
        length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(length)
        time.sleep(0.15)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"accepted":true}')

    def log_message(self, format, *args):
        pass


async def scenario():
    server = ThreadingHTTPServer(("127.0.0.1", 0), SlowAcceptedHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    old = {key: os.environ.get(key) for key in (
        "JARVIS_N8N_WEBHOOK_URL", "JARVIS_N8N_TIMEOUT",
        "JARVIS_TWENTY_URL", "JARVIS_TWENTY_API_KEY", "JARVIS_TWENTY_TIMEOUT",
    )}
    try:
        SlowAcceptedHandler.calls = 0
        url = f"http://127.0.0.1:{server.server_port}"
        os.environ["JARVIS_N8N_WEBHOOK_URL"] = url
        os.environ["JARVIS_N8N_TIMEOUT"] = "0.02"
        result = await N8NAdapter().run({"mission_id": "m", "goal": "send", "step": {}, "context": {}})
        assert not result.ok
        assert not result.retryable
        assert "outcome unknown" in result.error.lower()

        os.environ["JARVIS_TWENTY_URL"] = url
        os.environ["JARVIS_TWENTY_API_KEY"] = "test-key"
        os.environ["JARVIS_TWENTY_TIMEOUT"] = "0.02"
        result = await TwentyAdapter().run({
            "mission_id": "m", "goal": "crm", "step": {},
            "context": {"company": "Acme"},
        })
        assert not result.ok
        assert not result.retryable
        assert "outcome unknown" in result.error.lower()
        assert SlowAcceptedHandler.calls >= 2
    finally:
        server.shutdown()
        server.server_close()
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def main():
    asyncio.run(scenario())
    print("JARVIS-NEXT AMBIGUOUS HTTP TIMEOUT CONTRACT OK")


if __name__ == "__main__":
    main()
