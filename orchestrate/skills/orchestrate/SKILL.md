---
name: orchestrate
description: >-
  Coordinate explicitly requested, decomposable work through native Codex
  subagents with deliberate model and reasoning selection, bounded parallelism,
  structured handoffs, verification, and parent-owned synthesis. Use only when
  the user invokes $orchestrate, names Orchestrate, or directly asks to use this
  plugin. Do not trigger merely because a task is large or parallelizable. Do
  not use for small sequential tasks, deployed agent applications, persistent
  pipelines, OpenAI Agents SDK services, or Responses API multi-agent
  implementations.
---

# Orchestrate

Keep the main agent responsible for the objective, decisions, integration, and
final answer. Delegate bounded supporting work only when it improves speed,
specialization, evidence quality, or context hygiene.

Use only on OpenAI Codex hosts exposing native subagent spawn and supervision
tools. If those tools are unavailable, stay single-agent instead of falling
back to a thread-management workaround, custom runtime, or API multi-agent
system. Treat effective-route metadata as a separate host capability: record
the requested route for every child, and call the effective route verified only
when the parent can inspect host-provided evidence.

Loading this skill does not independently authorize delegation. Delegate only
when the current request explicitly invokes Orchestrate or an applicable
higher-priority instruction explicitly requires subagents. An explicit
invocation asks you to evaluate delegation; it does not require spawning for a
small or sequential task.

## Decide whether to delegate

Delegate when at least one condition holds:

- Two or more independent slices can run concurrently.
- A specialist has materially better instructions, tools, or model fit for a
  bounded slice.
- Exploration, logs, tests, or research would add substantial noise to the main
  context.
- Independent verification meaningfully reduces risk.

Stay single-agent when the task is small, sequential, clarification-bound, or
likely to create more coordination than useful work. Do not manufacture roles
to make the workflow look busy. Each child consumes its own model and tool
work, so the expected speed, quality, or context-hygiene benefit must earn the
extra cost.

## Establish the contract

Before spawning, record a compact orchestration contract:

- objective and done criteria
- constraints and approval boundaries
- current repository or artifact state
- task slices and their dependencies
- owner and write scope for every slice
- expected handoff and verification

Read [the task and handoff contract](references/task-contract.md) before
delegating. Read [the routing policy](references/routing-policy.md) whenever
choosing models, reasoning effort, custom agents, or concurrency.

## Build a shallow task graph

1. Split only on real knowledge, tool, or ownership boundaries.
2. Mark dependencies explicitly. Run only dependency-free slices together.
3. Keep the root as orchestrator and synthesizer.
4. Prefer direct children. Do not ask children to spawn descendants unless the
   user explicitly requests recursive delegation and the host supports it.
5. Start at most three direct children in one wave as a conservative local
   policy, then obey any tighter host cap and actual parent capacity. Current
   Codex configuration may expose
   `agents.max_concurrent_threads_per_session` for child threads, but use the
   current host's own accounting and limit.

Parallelize read-heavy research, exploration, testing, and review freely when
their scopes are independent. For writes, assign one owner per file or mutable
resource. Run overlapping write scopes sequentially or isolate them in separate
worktrees when the user requested that workflow.

## Route deliberately

Inspect the current spawn surface, available agent types, and model catalog
before choosing a route. Prefer, in order:

1. A named custom agent whose documented role, model, and tools match the
   slice.
2. A built-in agent with explicit `model` and host-exposed reasoning overrides
   when the spawn surface supports them.
3. A built-in agent with host-selected defaults when exact routing is not
   material.

Use only models exposed by the current host. Follow current official model
guidance and the routing policy rather than treating model names as permanent.
For custom-agent files, the documented `model` and
`model_reasoning_effort` settings take precedence. When they are absent,
documented resolution is explicit spawn settings, then `[agents]` defaults,
then the parent settings. A direct spawn surface can use a different field name
for reasoning; use only the field it actually exposes.

When the user requests an exact role or model, always record the requested
route. Record the observed route only from parent-visible host metadata. If the
host cannot prove it, label the result configuration-derived or unverified; do
not pretend the route succeeded. Stop the slice only when exact verification is
a required done criterion. Otherwise continue with reduced coverage disclosed.

When `fork_turns` is available, prefer `"none"` for bounded model-specific
children and pass an explicit task packet. The current public Codex docs do not
define `fork_turns`, so treat it as a host capability rather than a portable
contract. Include only the history the child genuinely needs.

## Spawn and supervise

For each child:

- Give one objective and one bounded scope.
- Include relevant paths, immutable refs, known facts, constraints, and done
  criteria.
- State whether edits are allowed and name the exact write scope.
- Require evidence: files inspected, commands run, sources used, or checks
  completed.
- Forbid nested delegation unless it is part of the approved task graph.

Start independent children in the same wave. Continue useful parent-owned work
while they run. Use follow-up messages for small corrections; interrupt only
when the route, scope, or safety boundary is wrong. Wait for all required
handoffs before integration.

Child threads inherit the parent's current tool access, filesystem view,
sandbox, permission boundary, and live runtime overrides. Custom-agent
configuration can provide defaults only where the current host supports them;
do not assume it creates a narrower boundary than the parent. Delegation is
coordination, not isolation. Set the parent permission mode appropriately
before delegation. Keep pushes, deployments, messages, account changes, and
other external side effects approval-gated and parent-owned unless the user
explicitly assigned them elsewhere.

## Verify and integrate

Treat child output as evidence, not authority.

1. Check every handoff against its done criteria.
2. Inspect material claims, diffs, and test results before relying on them.
3. Resolve contradictions from primary evidence or a focused verifier.
4. Confirm the worktree or source identity did not drift during parallel work.
5. Have the designated integrator make or reconcile overlapping changes.
6. Run the narrowest complete verification for the integrated result.
7. Return one coherent result, not a transcript dump.

If a required child fails, retry once only when the failure is plausibly
transient and the retry remains useful. Otherwise continue with reduced
coverage when safe and disclose it, or stop when the missing slice blocks a
credible result.

## Output

Report:

- the task graph actually used
- requested routing and its runtime-verified, configuration-derived, or
  unverified status when model choice mattered
- completed handoffs and verification
- any reduced coverage, conflicts, or unverified assumptions
- the integrated outcome and remaining user action

Do not claim concurrency, agent identity, model selection, verification, or
completion without observable evidence.
