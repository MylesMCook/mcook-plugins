---
name: thermo-nuclear-code-quality-review
description: >-
  Run one strict, change-scoped maintainability review for structural
  simplification, boundary ownership, branching growth, file sprawl, type
  clarity, and testability. Use explicitly for this single lens. Do not use for
  a paired Thermos review, an ordinary style review, or open-ended refactoring.
---

# Thermo nuclear code-quality review

Audit the supplied change without editing it. Correct behavior is necessary,
but the change must also avoid leaving the codebase harder to understand,
verify, operate, or extend.

## Review boundary

- Follow the supplied scope contract and report only costs introduced or
  materially worsened by the change.
- Do not spawn nested agents, edit files, or turn the review into a general
  redesign of untouched code.
- Skip formatting, naming, and cosmetic nits unless they hide a real invariant
  or ownership problem.

## Resolve missing scope

If the parent did not supply a scope contract, resolve one before reviewing:

1. Use explicit files, commit range, or diff from the user.
2. Otherwise use an explicit pull request and its base and head.
3. Otherwise review the current branch from its merge base with the detected
   remote-default branch.
4. Review staged, unstaged, and untracked work only when the user asks for
   uncommitted or current changes.

Exclude dirty worktree state from committed review. Record included paths,
exclusions, and a mode-specific identity using commit SHAs, diff hashes, or
sorted path and content hashes. Do not use a tracking upstream as the target
base unless explicit metadata identifies it that way.

## Review bar

Look for a code-judo move that preserves behavior while deleting concepts,
branches, wrappers, modes, or special cases. Prefer direct, boring code. Do not
invent an abstraction unless it reduces total complexity and has a clear owner.

Inspect the areas that apply:

- ad-hoc branches, flags, nullable modes, silent fallbacks, and scattered
  feature checks
- logic placed outside the module or layer that owns the concept
- thin wrappers, pass-through helpers, generic machinery, or duplicate helpers
  that add indirection without buying clarity
- cast-heavy, optional-heavy, or loosely typed boundaries that obscure the
  real invariant
- files pushed across roughly 1,000 lines by this change. Treat the threshold
  as a signal, not an automatic defect, and compare before versus after
- orchestration that serializes independent work or permits partial state when
  a simpler, more atomic structure is available
- changes that weaken testability, observability, failure isolation, or the
  ability to verify behavior again
- patches that treat a repeated symptom instead of fixing the owning boundary
  or root cause

## Questions

For each meaningful change, ask:

- Can a concrete alternative remove concepts instead of moving them?
- Is the logic owned by the right module and expressed at the right boundary?
- Does a type or state model make an illegal state impossible?
- Is each new abstraction earning its keep across the actual call sites?
- Does the change leave a replayable proof through tests, checks, or clear
  observability?

Do not report a structural complaint unless you can name the cost and a
credible simpler direction. "Consider refactoring" is not a finding.

## Output

Return candidate findings first. Use this shape for each one:

```text
[P2] Short imperative title
Confidence: 0.00-1.00
Location: path/to/file.ext:start-end
Structural cost: What becomes harder to own, reason about, or verify
Evidence: The added complexity and affected call sites
Simpler direction: A concrete deletion, boundary move, model, or decomposition
```

Prioritize structural regressions, missed simplifications, branching growth,
boundary and type problems, file-size growth, and testability. Then list checks
reviewed and residual risk. If no issue meets the bar, say
`No candidate maintainability findings.`
