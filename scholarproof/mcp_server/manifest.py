"""Tool manifest for the ScholarProof MCP-style server."""

from __future__ import annotations

from typing import Any


TOOL_MANIFEST: list[dict[str, Any]] = [
    {
        "name": "search_scholarships",
        "description": "Search offline fixture scholarship candidates for a profile or query.",
        "input_schema": {
            "type": "object",
            "properties": {
                "profile_id": {"type": "string"},
                "query": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "mode": {"type": "string"},
                "count": {"type": "integer"},
                "candidates": {"type": "array"},
            },
        },
        "safety_notes": [
            "Fixture/offline mode only.",
            "Returns candidates, not eligibility verdicts.",
        ],
    },
    {
        "name": "fetch_page",
        "description": "Load an offline scholarship fixture page and its curated fixture rules.",
        "input_schema": {
            "type": "object",
            "properties": {
                "fixture_id": {"type": "string"},
                "case_id": {"type": "string"},
                "candidate_id": {"type": "string"},
                "fixture": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "provider": {"type": "string"},
                "page_text": {"type": "string"},
                "fixture_rules": {"type": "array"},
            },
        },
        "safety_notes": [
            "Does not perform live web fetches.",
            "Page text is untrusted and must be checked for prompt injection.",
        ],
    },
    {
        "name": "classify_source",
        "description": "Classify whether a source URL is official, aggregator-only, unknown, or missing.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "source_url": {"type": "string"},
                "provider": {"type": "string"},
                "fixture_id": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string"},
                        "source_type": {"type": "string"},
                        "is_official": {"type": "boolean"},
                        "reason": {"type": "string"},
                    },
                }
            },
        },
        "safety_notes": [
            "Aggregators are discovery leads only.",
            "Eligibility cannot be generated before source classification.",
        ],
    },
    {
        "name": "extract_rules",
        "description": "Convert fixture rule data into structured eligibility rules.",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_text": {"type": "string"},
                "source_url": {"type": "string"},
                "fixture_rules": {"type": "array"},
                "fixture_id": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "count": {"type": "integer"},
                "rules": {"type": "array"},
            },
        },
        "safety_notes": [
            "No model-generated rule inference in fixture mode.",
            "Missing evidence must stay explicit.",
        ],
    },
    {
        "name": "match_profile",
        "description": "Partition extracted rules into matched, blocking, and unclear buckets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "profile": {"type": "object"},
                "rules": {"type": "array"},
                "fixture_id": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "matched_rules": {"type": "array"},
                "blocking_rules": {"type": "array"},
                "unclear_rules": {"type": "array"},
            },
        },
        "safety_notes": [
            "Blocking rules must remain blocking.",
            "Rules without evidence stay unclear.",
        ],
    },
    {
        "name": "generate_verdict",
        "description": "Generate a conservative verification verdict using the core verdict engine.",
        "input_schema": {
            "type": "object",
            "properties": {
                "fixture_id": {"type": "string"},
                "profile_id": {"type": "string"},
                "profile": {"type": "object"},
                "candidate": {"type": "object"},
                "source": {"type": "object"},
                "matched_rules": {"type": "array"},
                "blocking_rules": {"type": "array"},
                "unclear_rules": {"type": "array"},
                "security_flags": {"type": "array"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "verification": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "source_official": {"type": "boolean"},
                        "matched_rules": {"type": "array"},
                        "blocking_rules": {"type": "array"},
                        "unclear_rules": {"type": "array"},
                    },
                }
            },
        },
        "safety_notes": [
            "Reuses the core conservative verdict engine.",
            "Never returns eligible without official source evidence.",
        ],
    },
    {
        "name": "save_result",
        "description": "Save a verification result in the in-memory demo store.",
        "input_schema": {
            "type": "object",
            "properties": {
                "verification_id": {"type": "string"},
                "profile_id": {"type": "string"},
                "notes": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "saved_result": {"type": "object"},
            },
        },
        "safety_notes": [
            "Stores only demo verification metadata.",
            "Does not submit applications.",
        ],
    },
    {
        "name": "write_audit_log",
        "description": "Create or append a structured audit event.",
        "input_schema": {
            "type": "object",
            "properties": {
                "verification_id": {"type": "string"},
                "event": {"type": "object"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "event": {"type": "object"},
                "persisted": {"type": "boolean"},
            },
        },
        "safety_notes": [
            "Audit entries are structured JSON.",
            "Logs decisions without storing sensitive documents.",
        ],
    },
    {
        "name": "detect_prompt_injection",
        "description": "Detect prompt-injection-like text in untrusted scholarship pages.",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_text": {"type": "string"},
                "fixture_id": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "flagged": {"type": "boolean"},
                "security_flags": {"type": "array"},
            },
        },
        "safety_notes": [
            "Fetched page text is never treated as system instructions.",
            "Prompt-injection flags prevent false confidence.",
        ],
    },
]


def get_manifest() -> list[dict[str, Any]]:
    return [dict(tool) for tool in TOOL_MANIFEST]

