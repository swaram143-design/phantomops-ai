import asyncio
import os

from .ecosystem_adapters import N8NAdapter, TwentyAdapter


async def scenario():
    old = {
        key: os.environ.get(key)
        for key in (
            "JARVIS_N8N_WEBHOOK_URL",
            "JARVIS_N8N_TIMEOUT",
            "JARVIS_TWENTY_URL",
            "JARVIS_TWENTY_API_KEY",
            "JARVIS_TWENTY_TIMEOUT",
        )
    }
    try:
        # Port 9 is the discard service and is normally closed; using a very
        # small timeout keeps this contract deterministic without external I/O.
        os.environ["JARVIS_N8N_WEBHOOK_URL"] = "http://10.255.255.1:9/timeout"
        os.environ["JARVIS_N8N_TIMEOUT"] = "0.01"
        n8n = await N8NAdapter().run({"mission_id": "m", "goal": "timeout", "step": {}, "context": {}})
        assert not n8n.ok and n8n.retryable

        os.environ["JARVIS_TWENTY_URL"] = "http://10.255.255.1:9"
        os.environ["JARVIS_TWENTY_API_KEY"] = "test-key"
        os.environ["JARVIS_TWENTY_TIMEOUT"] = "0.01"
        twenty = await TwentyAdapter().run({
            "mission_id": "m",
            "goal": "timeout",
            "step": {},
            "context": {"company": "Acme"},
        })
        assert not twenty.ok and twenty.retryable
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def main():
    asyncio.run(scenario())
    print("JARVIS-NEXT HTTP ADAPTER TIMEOUT CONTRACT OK")


if __name__ == "__main__":
    main()
