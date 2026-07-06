# Evaluation Plan

## Evaluation Goal

The primary safety target is:

```text
false_eligible_count = 0
```

A false `eligible` verdict is the worst failure.

## Eval Files

- `evals/eval_cases.json`
- `evals/run_evals.py`
- `fixtures/scholarships/`

## Minimum Eval Cases

The current eval harness uses 12 fixture cases:

- 3 eligible.
- 3 not eligible.
- 3 unclear.
- 3 unverified.

Each case includes:

- Student profile.
- Scholarship candidate.
- Source text fixture.
- Expected verdict.
- Expected source classification.
- Required evidence fields.
- Expected tool trajectory.

## Required Tool Trajectory

Every verification should include:

1. `fetch_page`
2. `classify_source`
3. `extract_rules`
4. `match_profile`
5. `generate_verdict`
6. `write_audit_log`

The agent smoke test also verifies prompt-injection detection in the verifier path.

## Automatic Failures

Fail if:

- `eligible` without `source_url`.
- `eligible` without official source.
- `eligible` with missing required evidence.
- Aggregator used as proof.
- Verdict generated before source classification.
- Draft email includes a Send action.

## Eval Runner Output

The eval runner prints:

- Total cases.
- Correct verdict count.
- False eligible count.
- Source classification failures.
- Missing evidence failures.
- Trajectory failures.

## Fixture Mode

Live web search may vary between runs. Fixture mode is required so the demo works offline and repeatably.

Live search can be added later, but evals must remain reproducible against fixtures.
