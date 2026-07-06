"""Smoke test the FundMyDegree MCP-compatible stdio server."""

from __future__ import annotations

import json
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def _reader(stdout, output_queue: "queue.Queue[str]") -> None:
    for line in stdout:
        output_queue.put(line)


def _send(process: subprocess.Popen[str], message: dict[str, Any]) -> None:
    assert process.stdin is not None
    process.stdin.write(json.dumps(message) + "\n")
    process.stdin.flush()


def _read(output_queue: "queue.Queue[str]", timeout: float = 5.0) -> dict[str, Any]:
    try:
        line = output_queue.get(timeout=timeout)
    except queue.Empty as exc:
        raise AssertionError("Timed out waiting for MCP server response.") from exc
    return json.loads(line)


def main() -> int:
    process = subprocess.Popen(
        [sys.executable, "-m", "fundmydegree.mcp_server.protocol_server"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdout is not None
    output_queue: "queue.Queue[str]" = queue.Queue()
    thread = threading.Thread(target=_reader, args=(process.stdout, output_queue), daemon=True)
    thread.start()

    try:
        _send(
            process,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "fundmydegree-smoke", "version": "0.1.0"},
                },
            },
        )
        initialize = _read(output_queue)
        assert initialize["id"] == 1
        assert initialize["result"]["serverInfo"]["name"] == "fundmydegree-mcp-server"

        _send(process, {"jsonrpc": "2.0", "method": "notifications/initialized"})

        _send(process, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        tools_response = _read(output_queue)
        tools = tools_response["result"]["tools"]
        tool_names = {tool["name"] for tool in tools}
        assert "classify_source" in tool_names
        assert "generate_verdict" in tool_names
        assert len(tools) == 9

        _send(
            process,
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "classify_source",
                    "arguments": {"fixture_id": "eligible_01"},
                },
            },
        )
        call_response = _read(output_queue)
        assert call_response["id"] == 3
        result = call_response["result"]
        assert result["isError"] is False
        payload = json.loads(result["content"][0]["text"])
        assert payload["ok"] is True
        assert payload["output"]["source"]["is_official"] is True

        print("FundMyDegree MCP protocol smoke")
        print("initialize: ok")
        print(f"tools/list: {len(tools)} tools")
        print("tools/call classify_source: ok")
        print("passed: true")
        return 0
    finally:
        if process.stdin:
            process.stdin.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
