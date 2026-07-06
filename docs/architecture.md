# Architecture

FundMyDegree is a fixture-first scholarship matching and fit-checking prototype for international students.

The system is intentionally small:

1. A student fills My Profile in the React/Vite UI.
2. The FastAPI backend receives profile, search, verify, save, and draft-email requests.
3. The Root Orchestrator calls the Finder Agent and Verifier Agent.
4. The MCP-style tool layer exposes structured tools for search, source classification, rule extraction, profile matching, verdict generation, saving, audit logging, and prompt-injection detection.
5. The core verifier applies the conservative verdict policy.
6. The UI shows results as Best Matches, Need to Confirm, Not for You, or Couldn't Verify Yet.

## Diagrams

The README embeds the public diagrams stored in `docs/assets/`:

- `docs/assets/fundmydegree-system-architecture.png`
- `docs/assets/fundmydegree-conceptual-data-model.png`
- `docs/assets/fundmydegree-deployment-runtime-view.png`

## Components

### Student UI

Screens:

- My Profile.
- My Matches.
- Does this scholarship fit you?
- Why this match?
- Ask to confirm.
- Saved.

### Backend API

Routes:

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

### Root Orchestrator Agent

Coordinates the workflow. It never produces a final eligibility verdict without Verifier Agent output.

### Finder Agent

Finds candidate scholarships and returns structured candidate data. It does not decide eligibility.

### Verifier Agent

Handles:

- Source verification.
- Eligibility rule extraction.
- Profile matching.
- Conservative verdicting.
- Evidence generation.

### Clarification Email Skill

Drafts a safe email only when status is `unclear`. It never sends email.

### MCP-Style Tool Server

Exposes structured tools:

- `search_scholarships`
- `fetch_page`
- `classify_source`
- `extract_rules`
- `match_profile`
- `generate_verdict`
- `save_result`
- `write_audit_log`
- `detect_prompt_injection`

### In-Memory Fixture Store

Stores:

- Profiles.
- Candidates.
- Verification results.
- Clarification email drafts.
- Saved results.
- Audit events.

This is intentionally not a production database. It keeps the demo reproducible and avoids adding account or data-retention scope.

### Evaluation Runner

Runs fixture cases and enforces:

```text
false_eligible_count = 0
```
