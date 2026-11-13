# Orchestrate

Explicitly requested native subagent coordination for tasks that benefit from
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

This is a skills-only plugin. It uses only the host's native subagent tools
(Codex, Claude Code, Factory Droid, or any host with an equivalent); if they
are unavailable, it stays single-agent. The host owns the child threads,
permissions, and orchestration tools. No Agents SDK app, Responses API
multi-agent runtime, MCP server, daemon, hook, or API key is required.

## Use

Invoke the skill (`$orchestrate` in Codex, `/orchestrate:orchestrate` in Claude Code) or name
Orchestrate when you want the agent to evaluate a task
for delegation. The skill is explicit-only and will not activate merely because
a task is large or parallelizable. Small or sequential tasks still stay with
the main agent.

## Sources

- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://developers.openai.com/api/docs/guides/latest-model
- https://code.claude.com/docs/en/sub-agents
- https://docs.factory.ai/cli/configuration/custom-droids
- https://agentskills.io/specification

See `ATTRIBUTION.md` for upstream inspiration.
