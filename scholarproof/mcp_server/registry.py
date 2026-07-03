"""Tool registry for the ScholarProof MCP-style server."""

from __future__ import annotations

from typing import Any, Callable

from scholarproof.api import services

from .manifest import get_manifest
from . import tools
from .tools import ToolError


ToolFunction = Callable[[dict[str, Any]], dict[str, Any]]


TOOLS: dict[str, ToolFunction] = {
    "search_scholarships": tools.search_scholarships,
    "fetch_page": tools.fetch_page,
    "classify_source": tools.classify_source,
    "extract_rules": tools.extract_rules,
    "match_profile": tools.match_profile,
    "generate_verdict": tools.generate_verdict,
    "save_result": tools.save_result,
    "write_audit_log": tools.write_audit_log,
    "detect_prompt_injection": tools.detect_prompt_injection,
}


def list_tools() -> list[str]:
    return list(TOOLS)


def get_tool_manifest() -> list[dict[str, Any]]:
    return get_manifest()


def call_tool(name: str, input_data: dict[str, Any] | None = None) -> dict[str, Any]:
    if name not in TOOLS:
        return {
            "ok": False,
            "tool": name,
            "error": {
                "code": "tool_not_found",
                "message": f"Unknown tool: {name}.",
            },
        }

    try:
        output = TOOLS[name](input_data or {})
    except ToolError as exc:
        return {
            "ok": False,
            "tool": name,
            "error": {"code": exc.code, "message": exc.message},
        }
    except services.ApiError as exc:
        return {
            "ok": False,
            "tool": name,
            "error": {"code": f"api_{exc.status_code}", "message": exc.message},
        }

    return {
        "ok": True,
        "tool": name,
        "output": output,
    }

