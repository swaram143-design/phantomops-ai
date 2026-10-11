"""Minimal operator CLI for the integrated JARVIS stack."""

from __future__ import annotations

import argparse
import asyncio
import json

from .bootstrap import build_registry
from .permissions import PermissionEngine
from .runtime import JarvisRuntime
from .state import StateStore


def health():
    registry = build_registry()
    result = {}
    for worker in registry.workers.values():
        probe = getattr(worker, "health", None)
        result[worker.name] = probe() if callable(probe) else {"registered": True}
    print(json.dumps(result, indent=2, default=str))


async def mission(goal: str):
    runtime = JarvisRuntime(
        state=StateStore(),
        workers=build_registry(),
        permissions=PermissionEngine(),
    )
    result = await runtime.submit(goal)
    print(json.dumps(result, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(prog="jarvis-next")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("health", help="show registered workers and optional integration health")
    run = sub.add_parser("run", help="submit a durable mission")
    run.add_argument("goal", nargs="+", help="mission goal")
    args = parser.parse_args()
    if args.command == "health":
        health()
    else:
        asyncio.run(mission(" ".join(args.goal)))


if __name__ == "__main__":
    main()
