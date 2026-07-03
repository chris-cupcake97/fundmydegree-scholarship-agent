"""Smoke test the ScholarProof MCP-style tool layer."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scholarproof.api.store import store  # noqa: E402
from scholarproof.mcp_server.registry import call_tool, get_tool_manifest, list_tools  # noqa: E402


REQUIRED_TOOLS = {
    "search_scholarships",
    "fetch_page",
    "classify_source",
    "extract_rules",
    "match_profile",
    "generate_verdict",
    "save_result",
    "write_audit_log",
    "detect_prompt_injection",
}


def _load_case(case_id: str) -> dict:
    cases = json.loads((ROOT / "evals" / "eval_cases.json").read_text(encoding="utf-8"))
    for case in cases:
        if case["id"] == case_id:
            return case
    raise AssertionError(f"Missing fixture case: {case_id}")


def _tool(name: str, input_data: dict) -> dict:
    result = call_tool(name, input_data)
    assert result["ok"], f"{name} failed: {result}"
    assert isinstance(result["output"], dict), f"{name} returned non-object output"
    return result["output"]


def _run_stepwise_unclear_workflow() -> str:
    case = _load_case("unclear_01")
    page = _tool("fetch_page", {"fixture_id": case["id"]})
    source = _tool("classify_source", {"url": page["url"], "provider": page["provider"]})["source"]
    security = _tool("detect_prompt_injection", {"page_text": page["page_text"]})
    rules = _tool(
        "extract_rules",
        {
            "page_text": page["page_text"],
            "source_url": page["url"],
            "fixture_rules": page["fixture_rules"],
        },
    )
    matched = _tool(
        "match_profile",
        {
            "profile": case["profile"],
            "rules": rules["rules"],
        },
    )
    verification = _tool(
        "generate_verdict",
        {
            "profile": case["profile"],
            "candidate": case["candidate"],
            "source": source,
            "matched_rules": matched["matched_rules"],
            "blocking_rules": matched["blocking_rules"],
            "unclear_rules": matched["unclear_rules"],
            "security_flags": security["security_flags"],
        },
    )["verification"]

    assert verification["status"] == "unclear"
    assert verification["source_official"] is True
    assert verification["unclear_rules"] or verification["missing_required_rules"]
    return verification["id"]


def _assert_fixture_verdict(case_id: str, expected_status: str) -> dict:
    verification = _tool("generate_verdict", {"fixture_id": case_id})["verification"]
    assert verification["status"] == expected_status, (
        f"{case_id}: expected {expected_status}, got {verification['status']}"
    )
    return verification


def main() -> int:
    store.reset()

    manifest = get_tool_manifest()
    tool_names = set(list_tools())
    assert REQUIRED_TOOLS == tool_names
    assert {tool["name"] for tool in manifest} == REQUIRED_TOOLS
    for tool in manifest:
        assert "input_schema" in tool
        assert "output_schema" in tool
        assert "safety_notes" in tool

    search = _tool("search_scholarships", {"query": "Bristol"})
    assert search["mode"] == "fixture"
    assert search["count"] >= 1

    unclear_verification_id = _run_stepwise_unclear_workflow()
    saved = _tool(
        "save_result",
        {
            "verification_id": unclear_verification_id,
            "notes": "Needs official country eligibility clarification.",
        },
    )
    assert saved["saved_result"]["verification_id"] == unclear_verification_id

    audit = _tool(
        "write_audit_log",
        {
            "verification_id": unclear_verification_id,
            "event": {
                "step": "smoke",
                "tool": "smoke_tools",
                "input_summary": "append smoke audit event",
                "output_summary": "audit append verified",
            },
        },
    )
    assert audit["persisted"] is True

    unverified = _assert_fixture_verdict("unverified_01", "unverified")
    assert unverified["source_type"] == "aggregator_lead"
    assert unverified["source_official"] is False

    unclear = _assert_fixture_verdict("unclear_03", "unclear")
    assert "funding_amount" in unclear["missing_required_rules"]

    not_eligible = _assert_fixture_verdict("not_eligible_01", "not_eligible")
    assert not_eligible["blocking_rules"]

    eligible = _assert_fixture_verdict("eligible_01", "eligible")
    assert eligible["source_official"] is True
    assert eligible["source_url"]
    assert not eligible["missing_required_rules"]

    prompt = _tool("detect_prompt_injection", {"fixture_id": "unverified_01"})
    assert prompt["flagged"] is True

    print("ScholarProof tool smoke")
    print(f"manifest_tools: {len(manifest)}")
    print("search_scholarships: ok")
    print("stepwise_unclear_workflow: ok")
    print("aggregator_unverified: ok")
    print("missing_evidence_unclear: ok")
    print("blocking_not_eligible: ok")
    print("eligible_official_evidence: ok")
    print("save_result: ok")
    print("write_audit_log: ok")
    print("detect_prompt_injection: ok")
    print("passed: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

