# Orchestrate

Explicitly requested Codex subagent coordination for tasks that benefit from
deliberate delegation, model routing, bounded parallelism, and verified
synthesis.

## What it does

- Keeps the main agent responsible for decisions and the final result.
- Routes bounded supporting work to named custom agents or suitable models.
- Uses structured task packets and evidence-backed handoffs.
- Parallelizes independent work without allowing overlapping write ownership.
- Records requested routing and labels effective routing as runtime-verified,
  configuration-derived, or unverified.
- Treats delegation as coordination, never as sandbox or permission isolation.

This is a skills-only plugin. It uses only native Codex subagent tools; if they
are unavailable, it stays single-agent. Native Codex owns the child threads,
permissions, and orchestration tools. No Agents SDK app, Responses API
multi-agent runtime, MCP server, daemon, hook, or API key is required.

## Use

Invoke `$orchestrate` or name Orchestrate when you want Codex to evaluate a task
for delegation. The skill is explicit-only and will not activate merely because
a task is large or parallelizable. Small or sequential tasks still stay with
the main agent.

## Sources

- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://developers.openai.com/api/docs/guides/latest-model
- https://developers.openai.com/codex/use-cases
- https://agentskills.io/specification

See `ATTRIBUTION.md` for upstream inspiration.
