import asyncio
import sys

from .ecosystem_adapters import _run_command


async def scenario():
    ok = await _run_command([sys.executable, "-c", "print('ok')"], timeout=5)
    assert ok.ok
    assert ok.data["stdout"] == "ok"
    assert ok.data["exit_code"] == 0

    non_retryable = await _run_command([sys.executable, "-c", "import sys; sys.exit(1)"], timeout=5)
    assert not non_retryable.ok
    assert not non_retryable.retryable
    assert non_retryable.error == "exit 1"

    retryable = await _run_command([sys.executable, "-c", "import sys; sys.exit(124)"], timeout=5)
    assert not retryable.ok
    assert retryable.retryable
    assert retryable.error == "exit 124"

    timed_out = await _run_command([sys.executable, "-c", "import time; time.sleep(2)"], timeout=1)
    assert not timed_out.ok
    assert timed_out.retryable
    assert timed_out.error == "command timeout after 1s"

    missing = await _run_command(["jarvis-command-that-does-not-exist-9f1a"], timeout=5)
    assert not missing.ok
    assert not missing.retryable
    assert missing.error == "executable not found: jarvis-command-that-does-not-exist-9f1a"


def main():
    asyncio.run(scenario())
    print("JARVIS-NEXT COMMAND ADAPTER CONTRACT OK")


if __name__ == "__main__":
    main()
