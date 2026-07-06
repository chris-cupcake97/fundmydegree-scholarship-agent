# Final Capstone Requirements Checklist

This checklist maps FundMyDegree to the Kaggle capstone concepts without overstating what the prototype does.

## 1. Agent / Multi-Agent System

- Current implementation: ADK-style orchestrated multi-agent workflow in Python.
- Proof files:
  - `fundmydegree/agents/orchestrator.py`
  - `fundmydegree/agents/finder.py`
  - `fundmydegree/agents/verifier.py`
  - `fundmydegree/agents/clarification_email.py`
  - `scripts/smoke_agents.py`
- Risk level: medium.
- Action needed: In the writeup/video, describe this as an "ADK-style" workflow unless official Google ADK is added later.

## 2. MCP Server

- Current implementation: internal local tool registry plus a minimal MCP-compatible JSON-RPC stdio wrapper around the same tools.
- Proof files:
  - `fundmydegree/mcp_server/registry.py`
  - `fundmydegree/mcp_server/tools.py`
  - `fundmydegree/mcp_server/protocol_server.py`
  - `scripts/smoke_mcp_protocol.py`
  - `docs/mcp_server.md`
- Risk level: medium.
- Action needed: Demonstrate `python -B scripts/smoke_mcp_protocol.py` and describe it as a minimal MCP-compatible stdio wrapper, not production MCP infrastructure.

## 3. Security Features

- Current implementation: conservative verdict policy, official-source gate, prompt-injection detection, audit logs, no auto-send, no auto-submit, no sensitive document upload.
- Proof files:
  - `fundmydegree/core/security.py`
  - `fundmydegree/core/verdict_engine.py`
  - `fundmydegree/api/services.py`
  - `fundmydegree/ui/src/App.tsx`
  - `docs/security.md`
- Risk level: low.
- Action needed: Keep the video focused on the conservative safety choices.

## 4. Deployability

- Current implementation: local backend/frontend commands, Dockerfile, Docker Compose, `/health`, deployment smoke test, Cloud Run notes.
- Proof files:
  - `Dockerfile`
  - `docker-compose.yml`
  - `deploy/cloud-run.md`
  - `scripts/smoke_deploy.py`
  - `docs/deployment.md`
- Risk level: low.
- Action needed: Do not claim a public live deployment unless one is actually provided.

## 5. Agent Skills

- Current implementation: four focused skills for official source verification, rule extraction, conservative verdicting, and clarification email drafting.
- Proof files:
  - `.agent/skills/official-source-verification/SKILL.md`
  - `.agent/skills/eligibility-rule-extraction/SKILL.md`
  - `.agent/skills/conservative-verdicting/SKILL.md`
  - `.agent/skills/clarification-email-drafting/SKILL.md`
  - `docs/agent_skills.md`
- Risk level: low.
- Action needed: Mention skills in the writeup/video as routing guidance and safety constraints for the agent workflow.

## 6. Evaluation

- Current implementation: 12 golden fixture cases across eligible, not eligible, unclear, and unverified outcomes. Evals enforce `false_eligible_count = 0`.
- Proof files:
  - `evals/eval_cases.json`
  - `evals/run_evals.py`
  - `fixtures/scholarships/`
  - `docs/evaluation.md`
- Risk level: low.
- Action needed: Show eval output in the video.

## 7. Antigravity

- Current implementation: no repo change in this task.
- Proof files: final video/demo recording, not repository docs.
- Risk level: medium.
- Action needed: Out of scope for this task; final evidence should be handled in video/demo recording.
