"""Contract tests for the legacy orchestrator boundary.

The legacy core.Jarvis orchestrator remains available for compatibility, but
it is not the NEXUS executive authority. GOVI is the authority facade and
JARVIS-NEXT is the execution engine.
"""

import ast
from pathlib import Path


LEGACY_PATH = Path(__file__).resolve().parents[1] / "core" / "jarvis_orchestrator_v2.py"


def test_legacy_orchestrator_is_not_executive_authority():
    source = LEGACY_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    assert "class Jarvis" in source
    assert "GoviCore" not in source
    assert "JarvisRuntime" not in source

    # The compatibility orchestrator may dispatch its historical agents, but
    # it must not acquire or masquerade as the GOVI/JARVIS-NEXT authority.
    imported_names = {
        node.names[0].name
        for node in tree.body
        if isinstance(node, ast.Import)
    }
    assert "jarvis_next" not in imported_names


if __name__ == "__main__":
    test_legacy_orchestrator_is_not_executive_authority()
    print("LEGACY BOUNDARY CONTRACT OK")
