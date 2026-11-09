# Routing policy

Use this policy after deciding a task deserves delegation. Use only the native
Codex subagent spawn and supervision tools exposed by the current host. Do not
fall back to a thread-management workaround, custom runtime, or API multi-agent
implementation. Recheck current official documentation and the host's visible
model catalog when model availability or behavior may have changed. This is a
routing policy, not a security-boundary policy.

## Choose the lightest capable route

| Work | Default route | Reasoning |
| --- | --- | --- |
| Ambiguous architecture, integration, hard debugging, final synthesis | `gpt-5.6` or the host's equivalent such as `gpt-5.6-sol` | Start at `high`; use `xhigh`, `max`, or `ultra` only when both host support and task risk earn it |
| Bounded implementation, exploration, research, or test work | `gpt-5.6-terra` | `medium` by default; `low` for truly routine work |
| Straightforward, repetitive, or high-volume support work | `gpt-5.6-luna`, only when the host exposes it | `low` or `medium` |
| Existing workflow pinned to an older model | Its explicit model, such as `gpt-5.4` | Preserve the configured or requested effort |
| Fast, focused UI iteration | Codex-Spark, only when the host exposes it | Use the host-supported setting |
| Stable specialist workflow | Matching named custom agent | Follow its documented configuration precedence |

Current Codex guidance says to start demanding agents with `gpt-5.6` and use
`gpt-5.6-terra` for faster, lighter subagent work. Current OpenAI model
guidance maps the `gpt-5.6` alias to `gpt-5.6-sol`, and describes
`gpt-5.6-luna` as an efficient high-volume option. Codex-Spark is a separate
option for fast, focused UI iteration; it is not a general text-only routing
default. Availability varies by product, account, and current host.

Do not route by price or speed alone. Keep high-risk security, destructive
operations, subtle architecture, and final integration with a model capable of
the required judgment.

## Prefer role contracts over decorative names

Use a named custom agent when its description and configuration genuinely fit
the slice. Custom agents may configure `model`, `model_reasoning_effort`,
sandbox mode, tools, and skills. A custom-agent model or reasoning setting takes
precedence; without one, documented resolution is explicit spawn settings, then
`[agents]` defaults, then the parent settings. Direct spawn APIs can name the
reasoning field differently, so use only the current host's exposed field.

Built-in `explorer` is appropriate for read-heavy mapping; `worker` is
appropriate for scoped implementation; `default` is the fallback. A custom
agent with the same name as a built-in takes precedence, so inspect the current
host before assuming a built-in route.

If no matching named agent exists, use a built-in role plus explicit model and
reasoning fields when the spawn surface supports them. Never assume a task name
selects an agent role.

## Preserve the parent boundary

Child agents normally inherit the parent's current tool access, filesystem
view, sandbox, permission boundary, and live runtime overrides. A custom-agent
file can provide defaults where the host supports them, but it is not proof of
a narrower effective boundary. Do not use delegation as a security or
permission-isolation mechanism.

## Bound concurrency

- Default to no more than three direct children as a local policy, not a
  documented platform limit.
- Leave capacity for the parent and obey the tighter of the host's visible cap,
  `agents.max_concurrent_threads_per_session` when inspectable, and actual
  runtime capacity. The documented Codex setting counts child threads; a host
  can use different accounting.
- Prefer one wave of independent children over a recursive tree.
- Reduce concurrency for tool-heavy, rate-limited, or write-heavy work.
- Never let two children own the same mutable file or resource concurrently.

## Verify routing

Always retain:

- requested agent type, model, reasoning effort, and history mode
- configuration precedence used, if a custom agent or defaults apply
- any fallback used and why

Retain observed agent type, model, reasoning effort, and history mode only when
the parent can see host-provided evidence. Mark the verification status as
`runtime-verified`, `configuration-derived`, `unverified`, or `mismatch`.
Configuration-derived means the expected setting follows configuration
precedence; it is not proof of the effective runtime selection. Child
self-report is not proof.

If runtime evidence conflicts with the request, stop or reroute the slice. If
runtime evidence is unavailable, do not claim exact routing; stop only if exact
verification is an explicit done criterion, otherwise disclose reduced
coverage.

## Documentation basis

- Codex subagents and custom agents:
  https://learn.chatgpt.com/docs/agent-configuration/subagents
- OpenAI model guidance:
  https://developers.openai.com/api/docs/guides/latest-model
- Codex model use cases:
  https://developers.openai.com/codex/use-cases
- Agent Skills specification:
  https://agentskills.io/specification

`fork_turns` is intentionally treated as host-specific because it is exposed by
some current Codex spawn surfaces but is not defined in the public Codex docs.
