"""Tool registry and MCP-compatible wrapper for FundMyDegree agents."""

from .registry import call_tool, get_tool_manifest, list_tools

__all__ = ["call_tool", "get_tool_manifest", "list_tools"]
