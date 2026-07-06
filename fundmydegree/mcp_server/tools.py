"""Structured FundMyDegree tools for agent use."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from fundmydegree.api import services
from fundmydegree.api.store import store
from fundmydegree.core.models import (
    AuditEvent,
    EligibilityRule,
    ScholarshipCandidate,
    SourceClassification,
    StudentProfile,
)
from fundmydegree.core.rule_extraction import extract_rules as core_extract_rules
from fundmydegree.core.rule_extraction import match_profile as core_match_profile
from fundmydegree.core.security import detect_prompt_injection as core_detect_prompt_injection
from fundmydegree.core.source_classifier import classify_source as core_classify_source
from fundmydegree.core.verdict_engine import generate_verdict as core_generate_verdict


ROOT = Path(__file__).resolve().parents[2]


class ToolError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _case_from_input(input_data: dict[str, Any]) -> dict[str, Any]:
    fixture_id = input_data.get("fixture_id") or input_data.get("case_id")
    candidate_id = input_data.get("candidate_id")
    fixture = input_data.get("fixture")

    if fixture:
        for case in services._load_eval_cases():
            if case.get("fixture") == fixture:
                return copy.deepcopy(case)
        raise ToolError("fixture_not_found", f"No fixture case found for {fixture}.")

    if fixture_id or candidate_id:
        try:
            return copy.deepcopy(
                services._find_case(
                    fixture_id=str(fixture_id) if fixture_id else None,
                    candidate_id=str(candidate_id) if candidate_id else None,
                )
            )
        except services.ApiError as exc:
            raise ToolError("fixture_not_found", exc.message) from exc

    raise ToolError("missing_fixture", "Provide fixture_id, case_id, candidate_id, or fixture.")


def _fetch_fixture(case: dict[str, Any]) -> dict[str, Any]:
    fixture_path = ROOT / "fixtures" / "scholarships" / case["fixture"]
    if not fixture_path.exists():
        raise ToolError("fixture_file_not_found", f"Missing fixture file: {case['fixture']}.")
    fixture = _load_json(fixture_path)
    return {
        "mode": "fixture",
        "fixture_id": case["id"],
        "fixture": case["fixture"],
        "url": str(fixture.get("url", case["candidate"].get("candidate_url", ""))),
        "provider": str(fixture.get("provider", case["candidate"].get("provider", ""))),
        "page_text": str(fixture.get("page_text", "")),
        "fixture_rules": list(fixture.get("rules", [])),
        "candidate": case["candidate"],
        "profile": case["profile"],
    }


def _rules_from_dicts(rules: list[dict[str, Any]]) -> list[EligibilityRule]:
    return [
        EligibilityRule.from_mapping(rule, source_url=str(rule.get("source_url", "")))
        for rule in rules
    ]


def _audit_events_from_dicts(events: list[dict[str, Any]]) -> list[AuditEvent]:
    audit_events: list[AuditEvent] = []
    for index, event in enumerate(events, start=1):
        audit_events.append(
            AuditEvent(
                step=str(event.get("step", index)),
                tool=str(event.get("tool", "tool_call")),
                input_summary=str(event.get("input_summary", "")),
                output_summary=str(event.get("output_summary", "")),
                success=bool(event.get("success", True)),
            )
        )
    return audit_events


def search_scholarships(input_data: dict[str, Any]) -> dict[str, Any]:
    return services.search_scholarships(input_data)


def fetch_page(input_data: dict[str, Any]) -> dict[str, Any]:
    case = _case_from_input(input_data)
    return _fetch_fixture(case)


def classify_source(input_data: dict[str, Any]) -> dict[str, Any]:
    if input_data.get("fixture_id") or input_data.get("case_id") or input_data.get("candidate_id"):
        page = fetch_page(input_data)
        url = page["url"]
        provider = page["provider"]
    else:
        url = str(input_data.get("url") or input_data.get("source_url") or "")
        provider = str(input_data.get("provider", ""))

    source = core_classify_source(
        url=url,
        provider=provider,
        config_path=ROOT / "config" / "trusted_sources.yml",
    )
    return {"source": source.to_dict()}


def extract_rules(input_data: dict[str, Any]) -> dict[str, Any]:
    if input_data.get("fixture_id") or input_data.get("case_id") or input_data.get("candidate_id"):
        page = fetch_page(input_data)
        page_text = page["page_text"]
        source_url = page["url"]
        fixture_rules = page["fixture_rules"]
    else:
        page_text = str(input_data.get("page_text", ""))
        source_url = str(input_data.get("source_url") or input_data.get("url") or "")
        fixture_rules = list(input_data.get("fixture_rules", []))

    rules = core_extract_rules(
        page_text=page_text,
        source_url=source_url,
        fixture_rules=fixture_rules,
    )
    return {"count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def match_profile(input_data: dict[str, Any]) -> dict[str, Any]:
    if "profile" in input_data:
        profile_data = input_data["profile"]
    else:
        profile_data = _case_from_input(input_data)["profile"]

    rules_data = input_data.get("rules")
    if rules_data is None:
        rules_data = extract_rules(input_data)["rules"]

    profile = StudentProfile.from_mapping(profile_data)
    matched, blocking, unclear = core_match_profile(profile, _rules_from_dicts(list(rules_data)))
    return {
        "matched_count": len(matched),
        "blocking_count": len(blocking),
        "unclear_count": len(unclear),
        "matched_rules": [rule.to_dict() for rule in matched],
        "blocking_rules": [rule.to_dict() for rule in blocking],
        "unclear_rules": [rule.to_dict() for rule in unclear],
    }


def detect_prompt_injection(input_data: dict[str, Any]) -> dict[str, Any]:
    if input_data.get("fixture_id") or input_data.get("case_id") or input_data.get("candidate_id"):
        page_text = fetch_page(input_data)["page_text"]
    else:
        page_text = str(input_data.get("page_text", ""))
    flags = core_detect_prompt_injection(page_text)
    return {"flagged": bool(flags), "security_flags": flags}


def generate_verdict(input_data: dict[str, Any]) -> dict[str, Any]:
    if input_data.get("fixture_id") or input_data.get("case_id") or input_data.get("candidate_id"):
        result = services.verify_scholarship(input_data)["verification"]
        return {"verification": result}

    profile = StudentProfile.from_mapping(dict(input_data.get("profile", {})))
    candidate = ScholarshipCandidate.from_mapping(dict(input_data.get("candidate", {})))
    source_data = dict(input_data.get("source", {}))
    source = SourceClassification(
        url=str(source_data.get("url", "")),
        domain=str(source_data.get("domain", "")),
        source_type=str(source_data.get("source_type", "unknown")),
        is_official=bool(source_data.get("is_official", False)),
        reason=str(source_data.get("reason", "")),
    )

    matched_rules = _rules_from_dicts(list(input_data.get("matched_rules", [])))
    blocking_rules = _rules_from_dicts(list(input_data.get("blocking_rules", [])))
    unclear_rules = _rules_from_dicts(list(input_data.get("unclear_rules", [])))
    security_flags = [str(flag) for flag in input_data.get("security_flags", [])]
    audit_log = _audit_events_from_dicts(list(input_data.get("audit_log", [])))

    result = core_generate_verdict(
        profile=profile,
        candidate=candidate,
        source=source,
        matched_rules=matched_rules,
        blocking_rules=blocking_rules,
        unclear_rules=unclear_rules,
        security_flags=security_flags,
        audit_log=audit_log,
    ).to_dict()
    verification_id = result["id"]
    store.verifications[verification_id] = result
    store.verification_context[verification_id] = {
        "fixture_id": input_data.get("fixture_id"),
        "fixture": input_data.get("fixture"),
        "candidate": candidate.to_dict(),
        "profile": profile.to_dict(),
    }
    return {"verification": result}


def save_result(input_data: dict[str, Any]) -> dict[str, Any]:
    return services.save_result(input_data)


def write_audit_log(input_data: dict[str, Any]) -> dict[str, Any]:
    event_data = dict(input_data.get("event", {}))
    event = AuditEvent(
        step=str(event_data.get("step", "")),
        tool=str(event_data.get("tool", "manual_audit")),
        input_summary=str(event_data.get("input_summary", "")),
        output_summary=str(event_data.get("output_summary", "")),
        success=bool(event_data.get("success", True)),
    ).to_dict()

    verification_id = str(input_data.get("verification_id", "")).strip()
    persisted = False
    if verification_id:
        verification = store.verifications.get(verification_id)
        if not verification:
            raise ToolError("verification_not_found", f"Verification not found: {verification_id}.")
        verification.setdefault("audit_log", []).append(event)
        persisted = True

    return {
        "verification_id": verification_id or None,
        "event": event,
        "persisted": persisted,
    }
