import asyncio
import sys
import tempfile
import types

from .nexus_adapter import NexusLegacyAdapter


class FakeSupervisor:
    def __init__(self):
        self.calls = []

    def available_agents(self):
        return {"research", "lead"}

    async def execute(self, task):
        self.calls.append(task)
        return {"success": True, "echo_type": task["type"]}


def install_fake_nexus(root, supervisor):
    package = types.ModuleType("gram")
    package.__path__ = [root]
    module = types.ModuleType("gram.gram_supervisor")
    module.gram_supervisor = supervisor
    sys.modules["gram"] = package
    sys.modules["gram.gram_supervisor"] = module


async def main():
    with tempfile.TemporaryDirectory() as root:
        supervisor = FakeSupervisor()
        install_fake_nexus(root, supervisor)

        adapter = NexusLegacyAdapter(root)
        assert adapter.score({"step": {"capability": "research"}}) == 80
        assert adapter.score({"step": {"capability": "unknown"}}) == 0

        result = await adapter.run({
            "goal": "research opportunities",
            "step": {"capability": "research", "action": "research"},
            "context": {"source": "contract-test"},
        })

        assert result.ok, result
        assert result.data["echo_type"] == "research", result
        assert len(supervisor.calls) == 1, supervisor.calls
        assert supervisor.calls[0]["type"] == "research"
        assert supervisor.calls[0]["context"]["source"] == "contract-test"

        missing = await adapter.run({
            "goal": "unsupported",
            "step": {"capability": "not_a_nexus_agent", "action": "research"},
        })
        assert not missing.ok, missing
        assert "not available" in missing.error, missing

        print("JARVIS-NEXT NEXUS CONTRACT OK")


if __name__ == "__main__":
    asyncio.run(main())
