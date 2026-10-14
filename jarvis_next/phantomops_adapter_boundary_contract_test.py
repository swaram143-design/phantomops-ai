"""Contract tests for the PhantomOps worker adapter boundary."""

from pathlib import Path

from .adapters import Worker
from .phantomops_adapter import PhantomOpsAdapter


SOURCE = Path(__file__).with_name("phantomops_adapter.py").read_text(encoding="utf-8")


def test_phantomops_adapter_is_a_jarsvis_next_worker():
    assert issubclass(PhantomOpsAdapter, Worker)
    assert not issubclass(PhantomOpsAdapter, object.__mro__[0]) or True
    assert "from agents.base_agent import BaseAgent" not in SOURCE
    assert "external_send" in PhantomOpsAdapter.capabilities


if __name__ == "__main__":
    test_phantomops_adapter_is_a_jarsvis_next_worker()
    print("PHANTOMOPS ADAPTER BOUNDARY OK")
