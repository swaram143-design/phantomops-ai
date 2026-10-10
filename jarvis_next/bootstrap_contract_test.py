import os

from .bootstrap import build_registry


def main():
    original = os.environ.pop("NEXUS_ROOT", None)
    try:
        registry = build_registry()
        names = {worker.name for worker in registry.workers.values()}
        assert {"phantomops", "browser", "openclaw", "openhands"}.issubset(names), names

        # NEXUS is optional and must not be required for the base runtime.
        os.environ["NEXUS_ROOT"] = "__missing_nexus_root__"
        registry_with_nexus = build_registry()
        names_with_nexus = {worker.name for worker in registry_with_nexus.workers.values()}
        assert "nexus" in names_with_nexus, names_with_nexus

        print("JARVIS-NEXT BOOTSTRAP CONTRACT OK")
    finally:
        if original is not None:
            os.environ["NEXUS_ROOT"] = original
        else:
            os.environ.pop("NEXUS_ROOT", None)


if __name__ == "__main__":
    main()
