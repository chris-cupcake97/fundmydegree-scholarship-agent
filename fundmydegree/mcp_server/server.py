"""Small JSON command runner for the FundMyDegree MCP-style tool layer."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .registry import call_tool, get_tool_manifest


def _parse_tool_input(raw_parts: list[str]) -> dict[str, Any]:
    if not raw_parts:
        return {}

    if all("=" in part and not part.strip().startswith("{") for part in raw_parts):
        return {
            key: value
            for key, value in (part.split("=", 1) for part in raw_parts)
        }

    raw = " ".join(raw_parts)
    if raw.startswith("@"):
        raw = open(raw[1:], encoding="utf-8").read()

    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("Tool input must be a JSON object.")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FundMyDegree MCP-style tool runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List tool manifests")

    call_parser = subparsers.add_parser("call", help="Call one tool")
    call_parser.add_argument("tool_name")
    call_parser.add_argument("input", nargs="*")

    args = parser.parse_args(argv)

    if args.command == "list":
        print(json.dumps({"tools": get_tool_manifest()}, indent=2))
        return 0

    if args.command == "call":
        result = call_tool(args.tool_name, _parse_tool_input(args.input))
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
