# Kaggle Rubric Mapping

This file maps FundMyDegree to the capstone rubric without storing course notes, PDFs, or rubric screenshots in the repository.

## Track

Agents for Good.

FundMyDegree helps international students make safer, faster scholarship decisions by checking fit and evidence before they spend time applying.

## Required Concepts

| Concept | FundMyDegree Evidence | Notes |
|---|---|---|
| Agent / multi-agent system | `fundmydegree/agents/`, `scripts/smoke_agents.py` | ADK-style Python workflow. The repo does not currently import official Google ADK. |
| MCP Server | `fundmydegree/mcp_server/protocol_server.py`, `scripts/smoke_mcp_protocol.py` | Minimal MCP-compatible JSON-RPC stdio wrapper around the existing tools. |
| Security features | `docs/security.md`, `fundmydegree/core/security.py`, `fundmydegree/core/verdict_engine.py` | Official-source gate, prompt-injection detection, no auto-send, no auto-submit, no uploads. |
| Deployability | `Dockerfile`, `docker-compose.yml`, `docs/deployment.md`, `scripts/smoke_deploy.py` | Reproducible local/container demo. No public live deployment is claimed. |
| Agent Skills | `.agent/skills/`, `docs/agent_skills.md` | Four focused skills with trigger examples, output shape, and safety notes. |
| Antigravity | Video/demo evidence | Out of scope for repo hardening. Show usage in final recording if required. |

## Pitch Evidence

- Clear problem: international students waste time on scholarships that later prove ineligible, unclear, outdated, or unofficial.
- Clear value: the system helps answer "Is this scholarship worth my time?"
- Personal motivation is documented in `README.md`.
- Diagrams are included in `docs/assets/`.

## Implementation Evidence

- Core verifier: `fundmydegree/core/`
- API layer: `fundmydegree/api/`
- Agent layer: `fundmydegree/agents/`
- Tool registry and MCP-compatible wrapper: `fundmydegree/mcp_server/`
- Frontend: `fundmydegree/ui/`
- Evals: `evals/run_evals.py`
- Smoke tests: `scripts/`

## Safety Evidence

The project intentionally avoids:

- Live web search.
- Account/auth expansion.
- Payment or subscription logic.
- Sensitive document upload.
- Auto-send email.
- Auto-submit applications.
- Claims of guaranteed eligibility, admission, funding, or scholarship success.

The key evaluation target remains:

```text
false_eligible_count = 0
```
