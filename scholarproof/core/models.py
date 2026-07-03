"""Data models used by the ScholarProof verification engine."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal


VerdictStatus = Literal["eligible", "unclear", "not_eligible", "unverified"]
RuleStatus = Literal["matched", "blocking", "unclear"]


STATUS_LABELS: dict[str, str] = {
    "eligible": "Strong Fit",
    "unclear": "Needs Clarification",
    "not_eligible": "Not for You",
    "unverified": "Unverified Lead",
}


REQUIRED_RULE_TYPES: tuple[str, ...] = (
    "current_cycle",
    "nationality",
    "residence",
    "fee_status",
    "degree_level",
    "field",
    "funding_amount",
    "deadline",
    "application_process",
)


def utc_now_iso() -> str:
    """Return an ISO timestamp with an explicit UTC timezone."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class StudentProfile:
    id: str
    nationality: str
    residence: str
    fee_status: str
    degree_level: str
    field: str
    intake: str
    target_regions: list[str] = field(default_factory=list)
    funding_need_percent: int = 0
    need_living_stipend: bool = False
    academic_level: str = ""
    work_experience_years: int = 0
    research_experience: bool = False
    documents_available: list[str] = field(default_factory=list)

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "StudentProfile":
        return cls(
            id=str(data.get("id", "")),
            nationality=str(data.get("nationality", "")),
            residence=str(data.get("residence", "")),
            fee_status=str(data.get("fee_status", "unknown")),
            degree_level=str(data.get("degree_level", "")),
            field=str(data.get("field", "")),
            intake=str(data.get("intake", "")),
            target_regions=list(data.get("target_regions", [])),
            funding_need_percent=int(data.get("funding_need_percent", 0)),
            need_living_stipend=bool(data.get("need_living_stipend", False)),
            academic_level=str(data.get("academic_level", "")),
            work_experience_years=int(data.get("work_experience_years", 0)),
            research_experience=bool(data.get("research_experience", False)),
            documents_available=list(data.get("documents_available", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ScholarshipCandidate:
    id: str
    name: str
    provider: str
    country: str
    candidate_url: str
    discovered_from: str = "fixture"
    source_type: str = ""
    funding_text: str = ""
    deadline_text: str = ""
    raw_summary: str = ""

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "ScholarshipCandidate":
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            provider=str(data.get("provider", "")),
            country=str(data.get("country", "")),
            candidate_url=str(data.get("candidate_url", "")),
            discovered_from=str(data.get("discovered_from", "fixture")),
            source_type=str(data.get("source_type", "")),
            funding_text=str(data.get("funding_text", "")),
            deadline_text=str(data.get("deadline_text", "")),
            raw_summary=str(data.get("raw_summary", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SourceClassification:
    url: str
    domain: str
    source_type: str
    is_official: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EligibilityRule:
    rule_type: str
    requirement_text: str
    evidence_text: str
    status: RuleStatus = "unclear"
    source_url: str = ""
    confidence: float = 0.0

    @classmethod
    def from_mapping(cls, data: dict[str, Any], source_url: str = "") -> "EligibilityRule":
        status = str(data.get("status", "unclear"))
        if status not in {"matched", "blocking", "unclear"}:
            status = "unclear"
        return cls(
            rule_type=str(data.get("rule_type", "")),
            requirement_text=str(data.get("requirement_text", "")),
            evidence_text=str(data.get("evidence_text", "")),
            status=status,  # type: ignore[arg-type]
            source_url=str(data.get("source_url", source_url)),
            confidence=float(data.get("confidence", 0.0)),
        )

    @property
    def has_evidence(self) -> bool:
        return bool(self.evidence_text.strip() and self.source_url.strip())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AuditEvent:
    step: str
    tool: str
    input_summary: str
    output_summary: str
    success: bool = True
    timestamp: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class VerificationResult:
    id: str
    candidate_id: str
    profile_id: str
    status: VerdictStatus
    student_facing_status: str
    source_url: str
    source_official: bool
    source_type: str
    source_reason: str
    last_checked: str
    matched_rules: list[EligibilityRule] = field(default_factory=list)
    blocking_rules: list[EligibilityRule] = field(default_factory=list)
    unclear_rules: list[EligibilityRule] = field(default_factory=list)
    missing_required_rules: list[str] = field(default_factory=list)
    verdict_reason: str = ""
    security_flags: list[str] = field(default_factory=list)
    audit_log: list[AuditEvent] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["matched_rules"] = [rule.to_dict() for rule in self.matched_rules]
        data["blocking_rules"] = [rule.to_dict() for rule in self.blocking_rules]
        data["unclear_rules"] = [rule.to_dict() for rule in self.unclear_rules]
        data["audit_log"] = [event.to_dict() for event in self.audit_log]
        return data


def student_label_for(status: str) -> str:
    return STATUS_LABELS.get(status, "Needs Clarification")

