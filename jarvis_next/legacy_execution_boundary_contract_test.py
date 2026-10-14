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
        "core/workflow_engine.py",
        "core/jarvis_orchestrator.py",
    ):
        imports = _imports(ROOT / relative)
        assert "jarvis_next.govi_core" in imports, relative
        assert "core.jarvis_orchestrator_v2" not in imports, relative


def test_legacy_workflow_engine_no_longer_activates_local_agents():
    source = (ROOT / "core/workflow_engine.py").read_text(encoding="utf-8")
    assert "from core.agent_manager import" not in source
    assert "activate_agent(" not in source
    assert "GoviCore" in source
    assert "govi.submit" in source


def test_legacy_jarvis_orchestrator_has_no_independent_runtime():
    source = (ROOT / "core/jarvis_orchestrator.py").read_text(encoding="utf-8")
    assert "LegacyJarvisFacade" in source
    assert "GoviCore" in source
    assert "while True" not in source
    assert "input(" not in source
    assert "route_task(" not in source
    assert "JarvisRuntime" not in source


def test_legacy_queue_is_only_a_queue():
    source = (ROOT / "core/task_queue_v2.py").read_text(encoding="utf-8")
    assert "jarvis_orchestrator_v2" not in source
    assert "GoviCore" not in source


def test_legacy_desktop_scheduler_has_no_import_time_loop():
    path = ROOT / "automation/task_automation.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    top_level_loops = [node for node in tree.body if isinstance(node, (ast.For, ast.While))]
    assert not top_level_loops
    assert "run_scheduled_loop" in path.read_text(encoding="utf-8")


if __name__ == "__main__":
    test_compatibility_execution_surfaces_route_through_govi()
    test_legacy_workflow_engine_no_longer_activates_local_agents()
    test_legacy_jarvis_orchestrator_has_no_independent_runtime()
    test_legacy_queue_is_only_a_queue()
    test_legacy_desktop_scheduler_has_no_import_time_loop()
    print("LEGACY EXECUTION BOUNDARY CONTRACT OK")
