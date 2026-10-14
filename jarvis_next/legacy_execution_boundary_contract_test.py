"""Contract tests for legacy compatibility execution boundaries."""

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _imports(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


def test_compatibility_execution_surfaces_route_through_govi():
    for relative in (
        "core/autonomous_runtime.py",
        "core/execution_pipeline.py",
    ):
        imports = _imports(ROOT / relative)
        assert "jarvis_next.govi_core" in imports, relative
        assert "core.jarvis_orchestrator_v2" not in imports, relative


def test_legacy_queue_is_only_a_queue():
    source = (ROOT / "core/task_queue_v2.py").read_text(encoding="utf-8")
    assert "jarvis_orchestrator_v2" not in source
    assert "GoviCore" not in source


if __name__ == "__main__":
    test_compatibility_execution_surfaces_route_through_govi()
    test_legacy_queue_is_only_a_queue()
    print("LEGACY EXECUTION BOUNDARY CONTRACT OK")
