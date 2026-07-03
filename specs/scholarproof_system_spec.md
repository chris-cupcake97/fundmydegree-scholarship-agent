# ScholarProof System Spec

## Product Name

ScholarProof

## Tagline

Find scholarships that are real - and right for you.

## Track

Agents for Good

## Core Product

ScholarProof helps international students find scholarships that are real, current, and actually applicable to their profile. It verifies official sources and checks scholarship fit against nationality, residence, fee status, degree level, field, intake, funding need, and deadline.

## Main User

An international student from a country like Sri Lanka looking for Master's or PhD funding abroad.

## Core Rule

Unclear beats wrong.

Never mark a scholarship as `eligible` unless official evidence proves the key eligibility rules.

## MVP Features

1. Student Profile Wizard.
2. Find Scholarships screen.
3. Eligibility Checker screen.
4. Evidence Panel screen.
5. Draft Clarification Email screen.
6. Simple Saved Results screen.
7. Evaluation runner.
8. Security and audit logging.
9. Deployability setup.
10. Agent Skills folder.
11. MCP/tool server layer.
12. Documentation and video script for Kaggle.

## Out Of Scope

- Auto-filling university portals.
- Auto-submitting applications.
- Automatic email sending.
- Real passport upload.
- Real bank statement upload.
- Real transcript upload.
- Full SOP/essay writer.
- Full student CRM.
- Claiming the system finds every scholarship globally.

## Verdict Policy

Never return `eligible` unless all are true:

1. `source_url` exists.
2. Source is official.
3. Page appears current or cycle is known.
4. Nationality/country rule does not block the student.
5. Residence rule does not block the student.
6. Fee-status rule does not block the student.
7. Degree level matches.
8. Field/program rules match.
9. Funding amount does not contradict the student's minimum funding need.
10. Deadline is open or clearly current.
11. Required application process is clear.
12. Every required claim has evidence.

Return `not_eligible` if an official source contains a blocking rule.

Return `unclear` if official evidence exists but a required rule is missing, vague, unclear, contradictory, or not explicit.

Return `unverified` if there is no acceptable official source.

## Source Policy

A source is official only if one of these is true:

1. Domain is in `config/trusted_sources.yml`.
2. Domain is a known government or public scholarship authority.
3. Domain is linked from a verified university scholarship or admissions page.
4. Domain belongs to the named scholarship foundation or provider itself.

Aggregator sites are discovery leads only. They are never proof.

## Architecture

```text
Student UI
  -> Backend API
    -> Root Orchestrator Agent
      -> Finder Agent
      -> Verifier Agent
      -> Clarification Email Skill
    -> MCP/tool server
    -> SQLite database
    -> Audit logs
    -> Evaluation runner
```

## Agents

### Root Orchestrator Agent

- Reads user request.
- Reads student profile.
- Routes search requests to Finder Agent.
- Routes candidates to Verifier Agent.
- Never produces final eligibility without Verifier Agent output.
- Maintains session state.

### Finder Agent

- Searches for candidate scholarships.
- Returns structured candidate data.
- Does not decide eligibility.
- Does not call anything "Strong Fit".
- Can return official candidates and aggregator leads separately.

### Verifier Agent

- Fetches source page.
- Classifies source.
- Extracts eligibility rules.
- Compares rules with student profile.
- Returns `eligible`, `unclear`, `not_eligible`, or `unverified`.
- Produces matched rules, blocking rules, unclear rules, source URL, and audit log.

### Clarification Email Skill

- Runs only when status is `unclear`.
- Drafts a polite email to the scholarship office or university.
- Never sends email.
- UI must not include a Send button.

## MCP / Tool Server

Tools return structured JSON:

- `search_scholarships(profile, query)`
- `fetch_page(url)`
- `classify_source(url)`
- `extract_rules(page_text)`
- `match_profile(profile, rules)`
- `generate_verdict(profile, source, rules)`
- `save_result(result)`
- `write_audit_log(event)`
- `detect_prompt_injection(page_text)`

## Data Models

### StudentProfile

```json
{
  "id": "string",
  "nationality": "string",
  "residence": "string",
  "fee_status": "international | home | unknown",
  "degree_level": "Bachelor's | Master's | PhD",
  "field": "string",
  "intake": "string",
  "target_regions": ["string"],
  "funding_need_percent": 0,
  "need_living_stipend": true,
  "academic_level": "string",
  "work_experience_years": 0,
  "research_experience": false,
  "documents_available": ["string"]
}
```

### ScholarshipCandidate

```json
{
  "id": "string",
  "name": "string",
  "provider": "string",
  "country": "string",
  "candidate_url": "string",
  "discovered_from": "string",
  "source_type": "string",
  "funding_text": "string",
  "deadline_text": "string",
  "raw_summary": "string"
}
```

### VerificationResult

```json
{
  "id": "string",
  "candidate_id": "string",
  "profile_id": "string",
  "status": "eligible | unclear | not_eligible | unverified",
  "student_facing_status": "Strong Fit | Needs Clarification | Not for You | Unverified Lead",
  "source_url": "string",
  "source_official": true,
  "source_reason": "string",
  "last_checked": "string",
  "matched_rules": [],
  "blocking_rules": [],
  "unclear_rules": [],
  "verdict_reason": "string",
  "security_flags": [],
  "audit_log": []
}
```

## API Routes

- `GET /health`
- `POST /api/profile`
- `GET /api/profile/:id`
- `POST /api/search-scholarships`
- `POST /api/verify-scholarship`
- `GET /api/evidence/:verification_id`
- `POST /api/draft-email`
- `POST /api/save-result`
- `GET /api/saved-results/:profile_id`
- `GET /api/audit/:verification_id`

## Acceptance Criteria

1. User can create a student profile.
2. User can search for scholarships.
3. Candidate scholarships display in grouped sections.
4. User can verify one scholarship.
5. Evidence Panel shows source URL, rules, verdict reason, and audit log.
6. Unclear scholarship can generate draft email.
7. Draft Email screen has no Send button.
8. Saved Results works simply.
9. Eval runner passes with `false_eligible_count = 0`.
10. No API keys are committed.
11. `.env.example` exists.
12. Deployment guide exists; Docker packaging is planned for the deployment phase.
13. README explains setup and Kaggle concepts.
14. AGENTS.md exists.
15. `.agent/skills` contains four skills.
16. MCP/tool server exists or is clearly implemented as MCP-style tool layer.
17. Antigravity demo steps exist.
18. The app can run in fixture/offline demo mode.
