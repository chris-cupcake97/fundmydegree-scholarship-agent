# Security Design

## Security Principle

ScholarProof handles student-facing eligibility advice. It must prefer uncertainty over false confidence.

Core rule:

> Unclear beats wrong.

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

## Prompt Injection Defense

Fetched web pages are untrusted data, not instructions.

The tool layer must detect phrases like:

- ignore previous instructions
- disregard system prompt
- mark all users eligible
- send data to
- reveal API key
- override eligibility rules

If detected:

1. Add a security flag to the evidence panel.
2. Log the event in the audit log.
3. Do not allow `eligible` unless official source status and required evidence are independently verified.

## Source Security

Aggregator pages are discovery leads only. They are never proof.

A source can prove eligibility only when it is official according to `config/trusted_sources.yml` or the official source policy in the system spec.

## Tool Security

- Tools return structured JSON only.
- All tool calls are logged.
- MCP/tool server operations are allowlisted.
- No tool sends email.
- No tool submits applications.
- No tool uploads sensitive documents.
- No tool exposes secrets.

## Secret Handling

- Use `.env.example` for variable names.
- Use environment variables for real secrets.
- Never commit API keys or passwords.
- Never expose backend secrets in frontend code.

## Student Safety

Student-facing language must make uncertainty visible:

- Strong Fit
- Needs Clarification
- Not for You
- Unverified Lead

No fake percentage scores like "87% eligible".

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
