# FundMyDegree Video Script

Target length: 5 minutes.

## 1. Opening - Problem

International students searching for funding do not need another random scholarship list. They need to know which opportunities actually match their country, degree level, field, funding need, and timeline before they spend hours applying.

## 2. Solution

FundMyDegree helps students find scholarships that actually fit them. It matches a lightweight student profile against scholarship opportunities, then shows what fits, what needs confirmation, and what may not be worth their time.

Core rule: unclear beats wrong.

## 3. UI Walkthrough

Show:

1. My Profile.
2. My Matches.
3. Grouped results: Strong Match, Need to Confirm, Not for You, Couldn't Verify Yet.
4. Does this scholarship fit you?
5. Why this match?
6. Ask to confirm.
7. Saved.

## 4. Agent Architecture

Show the architecture diagram:

- Root Orchestrator Agent.
- Finder Agent.
- Verifier Agent.
- Clarification Email Skill.

Explain that the Finder Agent finds candidate scholarships, the Verifier Agent checks official evidence and profile fit, and the Root Orchestrator returns grouped results without inventing eligibility decisions.

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

FundMyDegree finds scholarships that actually fit you.
