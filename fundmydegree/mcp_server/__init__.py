"""MCP-style tool layer for FundMyDegree agents."""

from .registry import call_tool, get_tool_manifest, list_tools

__all__ = ["call_tool", "get_tool_manifest", "list_tools"]
