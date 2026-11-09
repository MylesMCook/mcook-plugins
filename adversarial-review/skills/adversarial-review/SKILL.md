---
name: adversarial-review
description: >-
  Run a momentum-first three-lens Codex review of an explicit or readily
  inferable diff, commit, branch, plan, plugin, or small file set. Use when the
  user explicitly asks for adversarial, independent, three-reviewer, or
  Skeptic/Architect/Minimalist review. Infer the target and launch immediately;
  never require the user to manage permission modes or reviewer mechanics.
---

# Adversarial Review

Infer the review target, immediately run exactly three independent reviewers
through native Codex Subagent V2, and synthesize only evidence-backed findings
into one useful verdict.

## Boundaries

- Review only. Do not edit files, stage changes, commit, open a pull request,
  post comments, or run a repair loop.
- Invocation is authorization to run the three reviewers. Never ask the user to
  switch permission modes, configure agents, choose models, or restate an
  inferable scope.
- Let reviewers use the inherited tool and approval surface to gather evidence:
  targeted tests, builds, linters, logs, and diagnostics are allowed. They must
  not implement fixes, commit, push, deploy, post externally, or intentionally
  edit the reviewed source.
- Use this only for an explicitly requested, high-scrutiny review. Route an
  ordinary quick review or a broad security audit to the narrower matching
  workflow instead.
- Use only the host's native Subagent V2 spawn, supervision, and wait tools. Do
  not fall back to a legacy agent interface, thread-management workaround,
  external reviewer tool, custom runtime, or single-agent simulation.
- The three lenses are prompts, not agent-profile names. A V2 `task_name`
  identifies the child task; it does not select an agent type.

## First Read

Before delegation, open these files completely:

- `references/reviewer-lenses.md`
- `references/reviewer-prompt.md`
- `references/subagent-review.md`
- `references/verdict-format.md`

If local project instructions materially affect the target, also read their
exact contents before prompting reviewers:

- nearest applicable `AGENTS.md`
- `brain/principles.md`, when present

## Infer One Exact Scope

Choose one target and one sentence of intent without asking the user to operate
the workflow. Prefer, in order:

1. The explicit plugin, patch, plan, file set, commit, branch, pull request, or
   last-turn boundary named by the user.
2. Tracked staged and unstaged changes relevant to the active request.
3. The current branch against its merge base with the detected default branch.
4. The active implementation plan or artifact being discussed.

Exclude unrelated dirty or untracked state rather than asking the user how to
separate it. If no meaningful target exists after these defaults, return
`CONTESTED` with `NO_REVIEWABLE_TARGET` in one concise response; do not begin a
clarification loop.

Build a compact scope contract for all three reviewers:

- intent and review mode
- repository root plus base/head or commit identifiers when applicable
- included files or supplied artifacts and explicit exclusions
- the smallest useful diff, plan, and 1-3 adjacent dependency files
- a content fingerprint of the reviewed patch, plan, or files when practical
- applicable project principles

## Run the Three-Lens Review

1. Inspect the active V2 spawn surface and launch as soon as the compact scope
   contract is ready. If V2 is missing or the trio cannot launch, return
   `CONTESTED` with `SUBAGENT_UNAVAILABLE`; do not ask the user to debug the
   agent system.
2. Before spawning, allocate one shared run number for this invocation:
   - inspect the current V2 agent tree under this parent task
   - choose the smallest positive integer `N` for which all three candidate
     names formed from the `skeptic_r`, `architect_r`, and `minimalist_r`
     prefixes plus the decimal digits of `N` are unreserved
   - treat running, completed, failed, and interrupted child names as reserved
   - use the same `N` for all three reviewers; never reuse bare role names or
     mix run numbers within a trio
3. Start exactly three fresh V2 children in the same parallel wave:
   - if `N` is `2`, use `task_name: "skeptic_r2"` with the Skeptic lens
   - if `N` is `2`, use `task_name: "architect_r2"` with the Architect lens
   - if `N` is `2`, use `task_name: "minimalist_r2"` with the Minimalist lens
   Substitute the selected decimal digits; never pass a placeholder or
   uppercase letter in a task name. Keep these internal run suffixes out of the
   normal verdict.
4. Prefer the V2 `default` agent with `gpt-5.6-terra` and `high` reasoning when
   those exact controls are exposed by the current host. This is a fast,
   read-heavy review route. Otherwise omit unsupported overrides and use the
   V2 host default without asking the user.
5. Set `fork_turns: "none"` when the active V2 surface exposes it. Give each
   child the same self-contained scope contract, intent, project principles,
   and evidence packet, but only its assigned lens.
6. Require each child to investigate actively: inspect adjacent code and run
   useful targeted tests, builds, linters, or diagnostics when they improve
   confidence. Forbid implementation, commits, external side effects, nested
   delegation, and durable review artifacts.
7. Give the child wave three minutes before considering interruption. At three
   minutes, continue unfinished children only while the parent has seen
   meaningful progress during the previous minute. Never exceed five total
   minutes unless the user explicitly asks for a deeper review. Interrupt
   stalled or over-budget children and synthesize the settled results.
8. Compare the post-review tracked-source fingerprint and `git status --short`
   with the pre-review state. Ignore expected test/build caches. Treat an
   unexplained change to reviewed source as `INCOMPLETE_COVERAGE`.

## Verify and Synthesize

Follow `references/verdict-format.md` exactly:

- verify that all three reviewer results exist, use their assigned lens, and
  are usable
- record missing, failed, timed-out, malformed, or incomplete reviewers under
  coverage
- reject weak, stale, out-of-scope, duplicate, or hand-wavy claims
- make a lead `accept` or `reject` judgment for every retained finding with a
  one-line rationale
- return only `PASS`, `CONTESTED`, or `REJECT` using the documented verdict
  logic
- discuss findings and next action, not permission modes, routing metadata, or
  agent mechanics unless one of those directly caused reduced coverage

## Defaults

- Exactly three fresh Codex subagents are required for a complete review.
- If any required reviewer cannot run or returns unusable output, return
  `CONTESTED` with an explicit coverage failure unless an accepted high-severity
  finding already requires `REJECT`.
- The active permission and approval settings never block review preflight. V2
  children inherit them. When automatic approval review is active, let it
  handle eligible child requests; never make the user configure it for this
  skill.
- Protect the user's momentum: infer sensible defaults, launch promptly, avoid
  setup dialogue, and return a compact decision.
- Do not create temporary review files by default; use returned child messages.

## Failure Labels

Use only these orchestration failure labels:

- `SUBAGENT_UNAVAILABLE`
- `SUBAGENT_FAILED`
- `TIMEOUT`
- `MALFORMED_OUTPUT`
- `INCOMPLETE_COVERAGE`
- `NO_REVIEWABLE_TARGET`
