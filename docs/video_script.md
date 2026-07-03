# ScholarProof Video Script

Target length: 5 minutes.

## 1. Opening - Problem

International students searching for funding do not need another random scholarship list. They need to know whether an opportunity is real, official, current, and actually right for their profile.

## 2. Solution

ScholarProof verifies official scholarship sources and checks eligibility against the student's nationality, residence, fee status, degree level, field, intake, funding need, and deadline.

Core rule: unclear beats wrong.

## 3. UI Walkthrough

Show:

1. Profile Wizard.
2. Find Scholarships.
3. Grouped results: Strong Fit, Needs Clarification, Not for You, Unverified Lead.
4. Eligibility Checker.
5. Evidence Panel.
6. Draft Clarification Email.
7. Saved Results.

## 4. Agent Architecture

Show the architecture diagram:

- Root Orchestrator Agent.
- Finder Agent.
- Verifier Agent.
- Clarification Email Skill.

Explain that the Verifier Agent handles source verification, rule extraction, profile matching, conservative verdicting, and evidence generation.

## 5. MCP / Tools

Show the MCP-style tools:

- `search_scholarships`
- `fetch_page`
- `classify_source`
- `extract_rules`
- `match_profile`
- `generate_verdict`
- `save_result`
- `write_audit_log`
- `detect_prompt_injection`

## 6. Security Features

Show:

- No auto-submit.
- No automatic email sending.
- No sensitive document uploads.
- Prompt-injection detection.
- Official-source gate.
- Audit log.
- No secrets in repo.

## 7. Eval Runner

Show fixture mode and eval output:

- Total cases.
- Correct verdict count.
- False eligible count.
- Source classification failures.
- Missing evidence failures.
- Trajectory failures.

Highlight:

```text
false_eligible_count = 0
```

## 8. Deployment

Show:

- `/health`
- Dockerfile.
- `.env.example`.
- Deployment docs.
- Fixture mode for reliable demo.
- Frontend build check.

## 9. Antigravity Usage

Show:

1. Repo opened in Google Antigravity.
2. System spec.
3. `AGENTS.md`.
4. UI inspection.
5. One UI issue fixed.
6. Diff reviewed before accepting.
7. App run locally.
8. Browser testing.
9. No YOLO auto-approve.

## 10. Closing Line

ScholarProof finds scholarships that are real - and right for you.
