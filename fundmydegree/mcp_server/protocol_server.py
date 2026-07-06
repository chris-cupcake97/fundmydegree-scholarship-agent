"""Minimal MCP-compatible stdio server for FundMyDegree tools.

This wrapper intentionally delegates to the existing local tool registry. It
does not replace the runtime path used by the FastAPI app or agents.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from .registry import call_tool, get_tool_manifest


SERVER_INFO = {
    "name": "fundmydegree-mcp-server",
    "version": "0.1.0",
}
DEFAULT_PROTOCOL_VERSION = "2024-11-05"


def _jsonrpc_result(message_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def _jsonrpc_error(message_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": message_id,
        "error": {"code": code, "message": message},
    }


def _write(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def _mcp_tools() -> list[dict[str, Any]]:
    tools = []
    for item in get_tool_manifest():
        tools.append(
            {
                "name": item["name"],
                "description": item["description"],
                "inputSchema": item.get("input_schema", {"type": "object"}),
            }
        )
    return tools


def _tool_call_result(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    result = call_tool(tool_name, arguments)
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(result, ensure_ascii=False, sort_keys=True),
            }
        ],
        "isError": not result.get("ok", False),
    }


def handle_message(message: dict[str, Any]) -> dict[str, Any] | None:
    """Handle a small, demo-oriented subset of MCP JSON-RPC methods."""

    message_id = message.get("id")
    method = message.get("method")
    params = message.get("params") or {}

    if message_id is None:
        # JSON-RPC notification. MCP clients commonly send initialized this way.
        return None

    if method == "initialize":
        requested_version = params.get("protocolVersion") or DEFAULT_PROTOCOL_VERSION
        return _jsonrpc_result(
            message_id,
            {
                "protocolVersion": requested_version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": SERVER_INFO,
            },
        )

    if method == "ping":
        return _jsonrpc_result(message_id, {})

    if method == "tools/list":
        return _jsonrpc_result(message_id, {"tools": _mcp_tools()})

    if method == "tools/call":
        tool_name = str(params.get("name", ""))
        arguments = params.get("arguments") or {}
        if not isinstance(arguments, dict):
            return _jsonrpc_error(message_id, -32602, "Tool arguments must be an object.")
        if not tool_name:
            return _jsonrpc_error(message_id, -32602, "Tool name is required.")
        return _jsonrpc_result(message_id, _tool_call_result(tool_name, arguments))

    return _jsonrpc_error(message_id, -32601, f"Unsupported MCP method: {method}.")


def main() -> int:
    for line in sys.stdin:
        raw = line.strip()
        if not raw:
            continue

        try:
            message = json.loads(raw)
        except json.JSONDecodeError as exc:
            _write(_jsonrpc_error(None, -32700, f"Invalid JSON: {exc.msg}."))
            continue

        if not isinstance(message, dict):
            _write(_jsonrpc_error(None, -32600, "JSON-RPC message must be an object."))
            continue

        response = handle_message(message)
        if response is not None:
            _write(response)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
