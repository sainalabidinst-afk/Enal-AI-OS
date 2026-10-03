#!/usr/bin/env python3
"""
Enal CLI — Decorator Chain Management Tool (RFC-0003)

Commands:
    python -m sdk.enal_cli list           List available decorators
    python -m sdk.enal_cli decorate       Build and run a decorator chain
    python -m sdk.enal_cli chain          Print the active decorator chain for an app

Examples:
    # List available decorators
    python -m sdk.enal_cli list

    # Build a chain: logging + caching + metrics around a demo app
    python -m sdk.enal_cli decorate --chain logging,caching,metrics --task '{"input": "hello"}'

    # Show active chain for an app
    python -m sdk.enal_cli chain --app-id my_app
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from backend.app.core.decorators import ChainBuilder, DecoratorRegistry, HotSwapManager


def cmd_list(args: argparse.Namespace) -> int:
    """List all available decorators."""
    decorators = DecoratorRegistry.list_available()
    print("Available Decorators:")
    print("-" * 40)
    for name in decorators:
        decorator_cls = DecoratorRegistry.get(name)
        if decorator_cls:
            version = getattr(decorator_cls, "version", "unknown")
            print(f"  {name} (v{version})")
    print("-" * 40)
    print(f"Total: {len(decorators)} decorators registered")
    return 0


def cmd_decorate(args: argparse.Namespace) -> int:
    """Build a decorator chain and execute a task."""
    if not args.chain:
        print("Error: --chain is required (comma-separated decorator names)")
        return 1

    decorator_names = [d.strip() for d in args.chain.split(",")]
    task: dict[str, Any] = json.loads(args.task) if args.task else {"input": "test"}

    builder = ChainBuilder()
    for name in decorator_names:
        builder.add(name)

    mock_app_cls = _get_mock_app_class()
    app = mock_app_cls(config={})

    try:
        chain = builder.build(app)
        result = chain.execute(task)
        print("Decorator Chain Built Successfully")
        print(f"  Chain: {' → '.join(decorator_names)} → BaseApp")
        print(f"  Result: {json.dumps(result, indent=2, default=str)}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


def cmd_chain(args: argparse.Namespace) -> int:
    """Print the active decorator chain for an app."""
    manager = HotSwapManager()
    active = manager.get_active(args.app_id)
    if active is None:
        print(f"No active decorator chain for app '{args.app_id}'")
        return 0

    print(f"Active Decorator Chain for '{args.app_id}':")
    current: object | None = active
    depth = 0
    while current is not None:
        name = getattr(current, "name", type(current).__name__)
        version = getattr(current, "version", "unknown")
        print(f"  [Layer {depth}] {name} v{version}")
        current = getattr(current, "_wrapped", None)
        if current is not None and not hasattr(current, "_invoke"):
            break
        depth += 1
    return 0


def _get_mock_app_class() -> type:
    """Import MockBaseApp lazily to avoid circular imports."""
    from backend.app.core.decorators.testing import MockBaseApp

    return MockBaseApp


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="enal-cli",
        description="Decorator Chain Management Tool (RFC-0003)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list
    list_parser = subparsers.add_parser("list", help="List available decorators")
    list_parser.set_defaults(func=cmd_list)

    # decorate
    decorate_parser = subparsers.add_parser("decorate", help="Build and run a decorator chain")
    decorate_parser.add_argument(
        "--chain",
        type=str,
        required=True,
        help="Comma-separated decorator names (e.g., 'logging,caching,metrics')",
    )
    decorate_parser.add_argument(
        "--task",
        type=str,
        default='{"input": "test"}',
        help="JSON task to execute",
    )
    decorate_parser.set_defaults(func=cmd_decorate)

    # chain
    chain_parser = subparsers.add_parser("chain", help="Print active decorator chain")
    chain_parser.add_argument(
        "--app-id",
        type=str,
        default="default",
        help="Application ID to inspect",
    )
    chain_parser.set_defaults(func=cmd_chain)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
