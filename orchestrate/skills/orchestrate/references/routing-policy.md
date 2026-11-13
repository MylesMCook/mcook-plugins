# Routing policy

Use this policy after deciding a task deserves delegation. Use only the native
subagent spawn and supervision tools exposed by the current host. Do not
fall back to a thread-management workaround, custom runtime, or API multi-agent
implementation. Recheck current official documentation and the host's visible
model catalog when model availability or behavior may have changed. This is a
routing policy, not a security-boundary policy.

## Choose the lightest capable route

Route by capability tier, then map the tier to a model the current host
actually exposes.

| Work | Tier | Reasoning |
| --- | --- | --- |
| Ambiguous architecture, integration, hard debugging, final synthesis | Frontier: the host's most capable general model | Start high; use the host's highest settings only when task risk earns it |
| Bounded implementation, exploration, research, or test work | Standard: the host's balanced default | Medium by default; low for truly routine work |
| Straightforward, repetitive, or high-volume support work | Fast: the host's small or efficient model, only when exposed | Low or medium |
| Existing workflow pinned to a specific model | That explicit model | Preserve the configured or requested effort |
| Stable specialist workflow | Matching named custom agent | Follow its documented configuration |

Example mappings, current when written and subject to change; confirm against
the host's model catalog before use:

- Codex: frontier `gpt-5.6`, standard `gpt-5.6-terra`, fast `gpt-5.6-luna`.
  Codex-Spark, only when the host exposes it, suits fast focused UI iteration.
- Claude Code: frontier `opus`, standard `sonnet`, fast `haiku` aliases.
- Hosts without per-child model selection: inherit the parent model and record
  the route as host-selected.

Availability varies by product, account, and current host.

Do not route by price or speed alone. Keep high-risk security, destructive
operations, subtle architecture, and final integration with a model capable of
the required judgment.

## Prefer role contracts over decorative names

Use a named custom agent when its description and configuration genuinely fit
the slice. Depending on the host, custom agents may configure model, reasoning
effort, sandbox, tools, and skills. A custom-agent setting normally takes
precedence over spawn-time choices, which take precedence over host defaults
and then the parent's settings; confirm the current host's documented order.
Spawn surfaces name these fields differently, so use only the fields the host
exposes.

Prefer a read-only exploration role for mapping, a general worker role for
scoped implementation, and the host's default role as the fallback (for
example Codex and Factory Droid `explorer`/`worker`, Claude Code
`Explore`/`general-purpose`). A custom agent can shadow a built-in name, so inspect the
current host before assuming a built-in route.

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
- Leave capacity for the parent and obey the tighter of the host's visible
  concurrency cap (for example Codex
  `agents.max_concurrent_threads_per_session`) and actual runtime capacity.
  Hosts count children differently.
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
- Claude Code subagents:
  https://code.claude.com/docs/en/sub-agents
- Factory Droid custom droids:
  https://docs.factory.ai/cli/configuration/custom-droids
- Agent Skills specification:
  https://agentskills.io/specification

History controls such as Codex `fork_turns` are host-specific capabilities,
not portable contracts.
