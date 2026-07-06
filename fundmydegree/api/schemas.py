"""Pydantic request schemas for the FundMyDegree API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ProfileRequest(BaseModel):
    id: str | None = None
    nationality: str = ""
    residence: str = ""
    fee_status: str = "unknown"
    degree_level: str = ""
    field: str = ""
    intake: str = ""
    target_regions: list[str] = Field(default_factory=list)
    funding_need_percent: int = 0
    need_living_stipend: bool = False
    academic_level: str = ""
    work_experience_years: int = 0
    research_experience: bool = False
    documents_available: list[str] = Field(default_factory=list)


class SearchScholarshipsRequest(BaseModel):
    profile_id: str | None = None
    query: str = ""


class VerifyScholarshipRequest(BaseModel):
    profile_id: str | None = None
    fixture_id: str | None = None
    case_id: str | None = None
    candidate_id: str | None = None
    profile: dict[str, Any] | None = None


class DraftEmailRequest(BaseModel):
    verification_id: str
    student_name: str | None = None
    recipient: str | None = None


class SaveResultRequest(BaseModel):
    verification_id: str
    profile_id: str | None = None
    notes: str = ""


def model_to_dict(model: BaseModel) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump(exclude_none=True)
    return model.dict(exclude_none=True)
