"""Conservative verdict generation for FundMyDegree."""

from __future__ import annotations

from .models import (
    REQUIRED_RULE_TYPES,
    AuditEvent,
    EligibilityRule,
    ScholarshipCandidate,
    SourceClassification,
    StudentProfile,
    VerificationResult,
    student_label_for,
    utc_now_iso,
)


def _matched_required_rule_types(matched_rules: list[EligibilityRule]) -> set[str]:
    return {
        rule.rule_type
        for rule in matched_rules
        if rule.rule_type in REQUIRED_RULE_TYPES and rule.has_evidence
    }


def missing_required_rules(matched_rules: list[EligibilityRule]) -> list[str]:
    matched_types = _matched_required_rule_types(matched_rules)
    return [rule_type for rule_type in REQUIRED_RULE_TYPES if rule_type not in matched_types]


def generate_verdict(
    profile: StudentProfile,
    candidate: ScholarshipCandidate,
    source: SourceClassification,
    matched_rules: list[EligibilityRule],
    blocking_rules: list[EligibilityRule],
    unclear_rules: list[EligibilityRule],
    security_flags: list[str],
    audit_log: list[AuditEvent],
) -> VerificationResult:
    """Generate a conservative verdict with hard stops before `eligible`."""

    missing_rules = missing_required_rules(matched_rules)

    if not source.url or not source.is_official:
        status = "unverified"
        reason = "No acceptable official source proves the scholarship rules."
    elif blocking_rules:
        status = "not_eligible"
        reason = "An official source contains at least one blocking eligibility rule."
    elif security_flags:
        status = "unclear"
        reason = "Official source was found, but the page contains prompt-injection-like text."
    elif unclear_rules or missing_rules:
        status = "unclear"
        reason = "Official evidence is incomplete for required eligibility rules."
    else:
        status = "eligible"
        reason = "Official source evidence supports every required eligibility rule."

    return VerificationResult(
        id=f"verification_{candidate.id}_{profile.id}",
        candidate_id=candidate.id,
        profile_id=profile.id,
        status=status,  # type: ignore[arg-type]
        student_facing_status=student_label_for(status),
        source_url=source.url,
        source_official=source.is_official,
        source_type=source.source_type,
        source_reason=source.reason,
        last_checked=utc_now_iso(),
        matched_rules=matched_rules,
        blocking_rules=blocking_rules,
        unclear_rules=unclear_rules,
        missing_required_rules=missing_rules,
        verdict_reason=reason,
        security_flags=security_flags,
        audit_log=audit_log,
    )
