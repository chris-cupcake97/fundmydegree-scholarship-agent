# Course Concept Notes

These notes summarize the course concepts used by FundMyDegree. Official Kaggle/Google course PDFs are not redistributed in this public repository.

## Day 1 - The New SDLC With Vibe Coding

Key planning implications:

- Move from casual vibe coding to agentic engineering: formal specs, architecture, tests, evaluations, and human oversight.
- Treat context engineering as the core skill: agents need the right source documents, rules, examples, tools, and constraints.
- Build a harness around the model: prompts, tools, memory/state, tests, evals, logs, and deployment controls.
- Keep humans in the conductor/orchestrator role for architecture, correctness, judgment, and release readiness.
- For FundMyDegree, the verification harness matters more than UI polish.

## Day 2 - Agent Tools and Interoperability

Key planning implications:

- MCP should standardize tool access instead of ad hoc integrations.
- Tools need discovery, configuration, connection, schema validation, and debugging with inspector-style workflows.
- Tool calls should be scoped, auditable, and shown to users when there is risk of data leakage.
- A2A concepts support a multi-agent architecture, but FundMyDegree should keep bounded specialist agents to avoid unnecessary complexity.
- For FundMyDegree, MCP should expose safe scholarship search, fetch, source verification, rule extraction, and profile matching tools.

## Day 3 - Agent Skills

Key planning implications:

- Skills are lightweight procedural memory: a folder with `SKILL.md` plus optional scripts, references, and assets.
- Use progressive disclosure so agents load specialist instructions only when relevant.
- Skills need evaluation: trigger quality, output quality, trajectory quality, token budget, and regression checks.
- Treat skills like dependencies: pin, audit, test, and avoid untrusted skill sources.
- For FundMyDegree, skills should cover official-source verification, eligibility extraction, conservative verdicting, evidence writing, and clarification emails.

## Day 4 - Security and Evaluation

Key planning implications:

- Agentic systems need sandboxing, supply-chain defenses, egress governance, and contextual authorization.
- Guard against hallucinated packages, MCP spoofing, prompt injection, and overbroad credentials.
- Use zero ambient authority: tools get only the permissions needed for the current task.
- Observability is required for evaluation: log sessions, tool calls, costs, latency, and verdict decisions.
- For FundMyDegree, the main safety issue is false eligibility. The eval gate must require zero false eligible verdicts.

## Day 5 - Spec-Driven Production Grade Development

Key planning implications:

- Keep specifications in the repo as the source of truth.
- Use behavior-driven scenarios before implementation so the agent does not guess.
- Build MCP tools with clear schemas and connect them through controlled clients.
- Use guardrails, sandboxing, human-in-the-loop review, AI-assisted tests, evaluation, policy checks, and prompt sanitization.
- For FundMyDegree, docs, evals, and conservative policy should be written before feature code.
