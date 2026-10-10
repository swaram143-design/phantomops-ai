import asyncio
from unittest.mock import patch

from .external_adapters import OpenHandsAdapter


class FakeProcess:
    returncode = 0

    async def communicate(self):
        return b"OpenHands completed task", b""

    def kill(self):
        raise AssertionError("test process should not be killed")


async def run_test():
    captured = {}

    async def fake_create(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return FakeProcess()

    with patch("jarvis_next.external_adapters.shutil.which", return_value="/usr/bin/openhands"):
        with patch("jarvis_next.external_adapters.asyncio.create_subprocess_exec", side_effect=fake_create):
            result = await OpenHandsAdapter().run({
                "goal": "Fix the failing test and run the test suite",
                "context": {"workspace": "."},
            })

    assert result.ok, result
    assert captured["args"][:3] == ("openhands", "--headless", "--task"), captured
    assert captured["args"][3] == "Fix the failing test and run the test suite", captured
    assert captured["kwargs"]["cwd"]
    assert result.data["returncode"] == 0, result
    print("JARVIS-NEXT OPENHANDS ADAPTER CONTRACT OK")


def main():
    asyncio.run(run_test())


if __name__ == "__main__":
    main()
