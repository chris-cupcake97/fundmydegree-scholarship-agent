"""Run fixture evals for the FundMyDegree verification engine."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fundmydegree.core.fixture_flow import verify_fixture_case  # noqa: E402


EXPECTED_TRAJECTORY = [
    "fetch_page",
    "classify_source",
    "extract_rules",
    "match_profile",
    "generate_verdict",
    "write_audit_log",
]


def _load_cases() -> list[dict[str, Any]]:
    return json.loads((ROOT / "evals" / "eval_cases.json").read_text(encoding="utf-8"))


def _audit_tools(result: dict[str, Any]) -> list[str]:
    return [event["tool"] for event in result["audit_log"]]


def _has_ordered_subsequence(items: list[str], expected: list[str]) -> bool:
    index = 0
    for item in items:
        if index < len(expected) and item == expected[index]:
            index += 1
    return index == len(expected)


def _eligible_has_all_evidence(result: dict[str, Any]) -> bool:
    if result["status"] != "eligible":
        return True
    if not result["source_url"] or not result["source_official"]:
        return False
    if result["missing_required_rules"]:
        return False
    if result["unclear_rules"] or result["blocking_rules"]:
        return False
    return all(rule["evidence_text"] and rule["source_url"] for rule in result["matched_rules"])


def run() -> int:
    cases = _load_cases()
    failures: list[str] = []
    correct_verdict_count = 0
    false_eligible_count = 0
    source_classification_failures = 0
    missing_evidence_failures = 0
    trajectory_failures = 0

    for case in cases:
        result = verify_fixture_case(case, ROOT).to_dict()
        case_id = case["id"]

        if result["status"] == case["expected_verdict"]:
            correct_verdict_count += 1
        else:
            failures.append(
                f"{case_id}: expected verdict {case['expected_verdict']}, got {result['status']}"
            )

        expected_source_type = case.get("expected_source_type")
        if expected_source_type and result["source_type"] != expected_source_type:
            source_classification_failures += 1
            failures.append(
                f"{case_id}: expected source type {expected_source_type}, got {result['source_type']}"
            )

        if result["status"] == "eligible" and case["expected_verdict"] != "eligible":
            false_eligible_count += 1
            failures.append(f"{case_id}: false eligible")

        if result["status"] == "eligible" and not _eligible_has_all_evidence(result):
            false_eligible_count += 1
            missing_evidence_failures += 1
            failures.append(f"{case_id}: eligible without complete official evidence")

        if result["source_type"] == "aggregator_lead" and (
            result["source_official"] or result["status"] == "eligible"
        ):
            source_classification_failures += 1
            failures.append(f"{case_id}: aggregator source was used as proof")

        tools = _audit_tools(result)
        if not _has_ordered_subsequence(tools, EXPECTED_TRAJECTORY):
            trajectory_failures += 1
            failures.append(f"{case_id}: missing required tool trajectory, got {tools}")

        if "generate_verdict" in tools and "classify_source" in tools:
            if tools.index("generate_verdict") < tools.index("classify_source"):
                trajectory_failures += 1
                failures.append(f"{case_id}: verdict generated before source classification")

    passed = not failures and false_eligible_count == 0
    print("FundMyDegree evals")
    print(f"total_cases: {len(cases)}")
    print(f"correct_verdict_count: {correct_verdict_count}")
    print(f"false_eligible_count: {false_eligible_count}")
    print(f"source_classification_failures: {source_classification_failures}")
    print(f"missing_evidence_failures: {missing_evidence_failures}")
    print(f"trajectory_failures: {trajectory_failures}")
    print(f"passed: {str(passed).lower()}")
    if failures:
        print("failures:")
        for failure in failures:
            print(f"- {failure}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(run())
