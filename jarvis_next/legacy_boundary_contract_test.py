"""Contract tests for the legacy orchestrator authority boundary.

The legacy core.Jarvis orchestrator remains available for compatibility, but
it is not the NEXUS executive authority. GOVI is the authority facade and
JARVIS-NEXT is the execution engine.

This test intentionally treats the legacy orchestrator as opaque source text.
It must not be imported or parsed: the compatibility file is outside the
canonical execution path and may contain historical syntax that is not part
of the supported runtime.
"""

from pathlib import Path


LEGACY_PATH = Path(__file__).resolve().parents[1] / "core" / "jarvis_orchestrator_v2.py"


def test_legacy_orchestrator_is_not_executive_authority():
    source = LEGACY_PATH.read_text(encoding="utf-8")

    assert "class Jarvis" in source
    assert "GoviCore" not in source
    assert "JarvisRuntime" not in source
    assert "jarvis_next" not in source


if __name__ == "__main__":
    test_legacy_orchestrator_is_not_executive_authority()
    print("LEGACY BOUNDARY CONTRACT OK")
