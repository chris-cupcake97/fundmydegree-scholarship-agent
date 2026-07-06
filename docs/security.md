# Security Design

## Security Principle

FundMyDegree handles student-facing scholarship fit guidance. It must prefer uncertainty over false confidence.

Core rule:

```text
Unclear beats wrong.
```

FundMyDegree provides evidence-backed scholarship fit guidance. It does not guarantee admission, funding, eligibility, or scholarship success. Final decisions belong to universities, governments, or scholarship providers.

## Official-Source Eligibility Gate

`eligible` is impossible without official source evidence.

- Official-source pages can support eligibility only when they satisfy the trusted-source policy.
- Aggregator sites are leads only, never proof.
- Aggregator-only findings become `unverified`.
- Missing key evidence for country, degree, or funding becomes `unclear`.
- Blocking official rules become `not_eligible`.

## Prompt Injection Defense

Fetched pages are treated as untrusted data, not instructions.

The tool layer detects prompt-injection phrases such as:

- ignore previous instructions
- disregard system prompt
- mark all users eligible
- send data to
- reveal API key
- override eligibility rules

When detected:

1. A security flag is added to the evidence panel.
2. The event is recorded in the audit log.
3. The conservative verdict gate still requires official evidence before `eligible`.

## Data Minimization

The MVP collects only lightweight profile fields:

- Nationality.
- Current residence.
- Fee status.
- Degree level.
- Field.
- Intake.
- Target countries or regions.
- Minimum funding need percentage.
- Living stipend need.
- Academic level.
- Work experience years.
- Research experience.
- Manual document checklist.

The MVP does not upload:

- Passports.
- Bank statements.
- Real transcripts.
- Degree certificates.
- Offer letters.
- Financial evidence.

The UI document section is a checklist only.

## Tool And Workflow Safety

- No tool sends email.
- No tool submits applications.
- No tool uploads sensitive documents.
- No university portal autofill exists.
- Clarification emails are draft-only and expose `send_allowed: false`.
- The frontend has no Send button.
- All tools return structured JSON.
- The MCP-compatible stdio wrapper delegates to the same safe tools.
- Verification steps are audit logged.
- No live web search is performed in the current fixture-mode implementation.

## Secret Handling

- `.env.example` is allowed for variable names only.
- Real `.env` files are ignored.
- API keys, passwords, service-account files, and private key files must not be committed.
- Backend secrets must not be exposed in frontend code.

## Fixture/Offline Reproducibility

FundMyDegree currently runs in fixture/offline mode for reproducible demos and evals. Live web search is intentionally out of scope for this version.

## Known Dependency Advisories

`npm audit` was reviewed on July 3, 2026. It reports a Vite/esbuild development-server advisory:

- `esbuild <=0.24.2`
- Vite depends on the affected esbuild range.
- The available npm fix requires `npm audit fix --force`, which would install a breaking Vite major version.

Decision: do not run `npm audit fix --force` during this cleanup. The current MVP uses local fixture/demo mode, the production build still passes, and the advisory is documented for a later dependency-hardening pass.

## Student Safety Language

Student-facing language must make uncertainty visible:

- Strong Match
- Need to Confirm
- Not for You
- Couldn't Verify Yet

Do not use fake percentage scores such as "87% eligible."

## Audit Logging

Audit events should include:

- Candidate found.
- Source fetched.
- Source classified.
- Prompt injection checked.
- Rules extracted.
- Profile matched.
- Verdict generated.
- Result saved.

Each event records step, tool, timestamp, input summary, output summary, and success.
