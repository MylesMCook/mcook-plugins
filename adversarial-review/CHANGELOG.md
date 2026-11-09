# Changelog

## 0.3.4 - 2026-08-24

- Added the portable Agent Plugins 1.0.0 manifest while retaining the Codex
  compatibility overlay.

## 0.3.3 - 2026-07-28

- Replace fixed reviewer task names with clean numeric-suffixed names such as
  `skeptic_r2`, `architect_r2`, and `minimalist_r2`, using one automatically
  selected shared run number.
- Skip names reserved by completed, failed, interrupted, running, or partial
  earlier runs so the skill can be invoked repeatedly in one parent task.
- Add deterministic regression coverage for the repeated-invocation contract.

## 0.3.2 - 2026-07-27

- Replace the blunt 90-second child-wave cap with an adaptive budget.
- Allow three minutes before considering interruption, continue meaningful
  recent progress up to five total minutes, and interrupt only stalled or
  over-budget reviewers.

## 0.3.1 - 2026-07-27

- Make the contract suite portable to the versioned installed-plugin cache by
  skipping the repo-only marketplace assertion when the catalog is not bundled.

## 0.3.0 - 2026-07-27

- Remove the parent read-only permission gate and never ask the user to switch
  modes before review.
- Treat explicit invocation as sufficient authorization to infer the narrowest
  relevant scope and immediately launch the V2 trio.
- Prefer the fast `gpt-5.6-terra` V2 route with high reasoning when exposed,
  while falling back to host defaults without user involvement.
- Cap the standard child wave at 90 seconds and interrupt unfinished reviewers
  instead of letting a smoke-sized review consume several minutes.
- Let reviewers use inherited tools and automatic approval handling for
  targeted tests, builds, linters, and diagnostics.
- Keep the boundary at unsolicited implementation and external side effects,
  with tracked-source fingerprints catching accidental edits.
- Make the normal verdict shorter and focused on findings plus the next action,
  with agent mechanics shown only when coverage fails.

## 0.2.0 - 2026-07-27

- Require the native Codex Subagent V2 spawn, supervision, and wait surface,
  with no legacy agent or task/thread workaround.
- Replace invalid hyphenated task names with V2-compatible underscore names.
- Prefer the current V2 `reviewer` route and keep a V2-only `default` route when
  that agent type is unavailable.
- Use fresh `fork_turns: "none"` child contexts when the active host exposes
  the field.
- Require a read-only parent before launch and state plainly that inherited
  permissions make delegation coordination, not isolation.
- Separate requested routing from parent-visible effective-route evidence.
- Add deterministic contract tests for the V2-only boundary.
- Make deterministic package and installed-cache checks the normal fast release
  gate; keep the costly live three-reviewer run optional.

## 0.1.0 - 2026-07-10

- Package the locally authored Adversarial Review skill for the
  `mcook-plugins-local` marketplace.
- Preserve the mandatory Skeptic, Architect, and Minimalist three-lens review
  contract and its `PASS`, `CONTESTED`, and `REJECT` verdicts.
- Add explicit review-scope selection, same-wave native child guidance, and
  scope-mutation coverage checks.
- Add ChatGPT desktop presentation metadata with implicit invocation disabled
  to prevent accidental three-subagent runs.
- Require an effective read-only parent or child boundary before the trio can
  launch, with scope/status comparison retained as audit evidence.
- Make fresh-task acceptance collision-safe when the legacy same-named local
  skill remains available for rollback.
- Add docs-backed design rationale and fresh-task eval guidance.
