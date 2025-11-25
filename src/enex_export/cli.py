"""CLI entry point for enex-export.

This module defines a small but robust command-line interface using
argparse. It is structured for easy extension with subcommands.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="enex-export",
        description="enex-export: command-line tool scaffold",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show the application version and exit",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # Example subcommand: hello
    hello = subparsers.add_parser(
        "hello",
        help="Print a friendly greeting (example subcommand)",
    )
    hello.add_argument(
        "--name",
        default="world",
        help="Name to greet (default: world)",
    )

    return parser


def _run_hello(name: str) -> int:
    print(f"Hello, {name}!")
    return 0


def _main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if getattr(args, "version", False):
        print(__version__)
        return 0

    if args.command == "hello":
        return _run_hello(args.name)

    # No command provided: show help
    parser.print_help()
    return 0


def main() -> None:
    """Console entry point used by the installed script.

    This function intentionally exits the interpreter with the return code
    from _main(), ensuring correct exit behavior when installed as a script.
    """
    sys.exit(_main(sys.argv[1:]))
