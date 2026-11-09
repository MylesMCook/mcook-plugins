# Codex Subagent V2 Review

## Contract

Run exactly three fresh native Codex Subagent V2 children in the same parallel
wave. Before any spawn call, inspect the current V2 agent tree under the parent
task and choose the smallest positive integer `N` for which all three names are
free. Construct the names from these prefixes plus the decimal digits of `N`:

- `skeptic_r`
- `architect_r`
- `minimalist_r`

For example, run `2` uses the exact valid task names `skeptic_r2`,
`architect_r2`, and `minimalist_r2`. Never pass a placeholder or uppercase
letter in a task name.
Running, completed, failed, and interrupted child names all remain reserved.
Use one shared run number for the whole trio. If any candidate is already
reserved, advance `N` for all three; never mix suffixes or reuse the bare role
names. This keeps repeated invocations in one parent task collision-free,
including after a partial earlier run.

The task name is an orchestration label, not an agent selector. Prefer the V2
`default` type with `gpt-5.6-terra` and `high` reasoning when the current host
exposes those exact controls. Otherwise use the V2 host default without asking
the user to choose. Each child receives the same scope and repo rules but a
different lens.

When V2 exposes `fork_turns`, use `"none"` and pass a complete compact scope
contract rather than inheriting the parent transcript. Start the three spawn
calls together, then use only V2 supervision and wait operations to collect all
three final results.

Keep run suffixes internal during a successful review. User-facing coverage
labels remain Skeptic, Architect, and Minimalist.

Do not use legacy agent tools, task or thread APIs as a surrogate, external
reviewer runtimes, or a parent-authored single-agent simulation. If native V2
cannot start the full trio, fail closed with `SUBAGENT_UNAVAILABLE`.

## Permissions And Momentum

V2 children inherit the parent task's tools, filesystem view, sandbox,
permission mode, approval handling, and live runtime overrides. That is useful:
reviewers may run targeted tests, builds, linters, and diagnostics to gather
stronger evidence. Do not block launch or ask the user to change modes.

When automatic approval review is active, let it evaluate eligible child
requests normally. The skill must not tell the user to toggle or manage that
setting. Reviewers still must not implement fixes, intentionally edit reviewed
source, commit, push, deploy, post externally, or delegate.

Do not narrate these mechanics during an ordinary successful review. The user
asked for findings, not an agent-runtime seminar.

For Git worktrees, record `git status --short` plus a content fingerprint of
the exact reviewed source before launch and compare both after all subagents
finish. Ignore ordinary build/test caches. An unexplained change to reviewed
source is `INCOMPLETE_COVERAGE`.

Use an adaptive total child-wave budget:

- allow three minutes before considering interruption
- after three minutes, continue only while unfinished children have produced
  parent-visible meaningful progress during the previous minute
- stop at five total minutes unless the user explicitly requested deeper review

Interrupt stalled or over-budget children and synthesize settled results with
explicit reduced coverage. If the host cannot spawn the trio, return
`CONTESTED` with
`SUBAGENT_UNAVAILABLE`. Do not use outside reviewer tools, a sequential
surrogate, or a single-agent fallback.

## Coverage Failures

A review has incomplete coverage when any required subagent:

- cannot be spawned
- fails before returning a final message
- times out
- returns empty or unusable output
- ignores the assigned lens or supplied scope
- implements a fix or changes reviewed source
- delegates to another agent

Classify the issue with one of:

- `SUBAGENT_UNAVAILABLE`
- `SUBAGENT_FAILED`
- `TIMEOUT`
- `MALFORMED_OUTPUT`
- `INCOMPLETE_COVERAGE`
- `NO_REVIEWABLE_TARGET`

Incomplete coverage forces `CONTESTED` unless there is already an accepted
high-severity finding, in which case return `REJECT`.

## Output Handling

Do not create `.tmp` review files by default. Use the subagents' returned final
messages. If the user explicitly asks to save reviewer artifacts, write only
after confirming the target location and keep artifacts out of committed source
unless requested.
