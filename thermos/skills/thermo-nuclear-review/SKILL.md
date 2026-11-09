---
name: thermo-nuclear-review
description: >-
  Run one change-scoped correctness and security review for bugs, breaking
  behavior, data loss, unsafe exposure, developer-experience regressions, and
  feature-gate leaks. Use explicitly for this single lens. Do not use for a
  paired Thermos review, a full-repository security scan, or remediation work.
---

# Thermo nuclear review

Audit one supplied branch, pull request, worktree snapshot, commit range, or
explicit file set. Remain read-only. The parent owns every repair.

## Review boundary

- Follow the supplied scope contract exactly.
- Report only defects introduced or materially worsened by the scoped change.
  A pre-existing issue is in scope only when the change makes it newly
  reachable, more severe, or security-relevant.
- Complete the independent audit before reading pull-request discussion.
- Do not edit files, post comments, or spawn nested agents.

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

## Audit the change

Trace each meaningful change through its callers, boundaries, state, and failure
paths. Check the areas that apply:

- functional behavior, performance regressions, error handling, invalid states,
  races, retries, and compatibility with existing callers
- data integrity, migrations, partial updates, backup assumptions, rollback,
  and recovery from interruption
- authentication, authorization, sessions, injection, unsafe defaults,
  privilege changes, secrets, and network or service exposure
- feature flags and internal, beta, tenant, or role gates
- availability, process supervision, health checks, observability, resource
  bounds, and remote-access failure modes
- developer experience, including environment variables, ports, dependencies,
  install steps, local startup, generated clients, and required services
- tests that should prove the changed behavior or failure path

## Finding bar

- Trace a reachable path end to end before reporting it.
- Finish research the repository can answer. Do not report an unresolved
  "unless another layer handles this" theory when that layer is available.
- Distinguish intended behavior from accidental blast radius.
- Calibrate priority from impact, reachability, and confidence. Intense wording
  does not make a finding severe.
- Skip cosmetic nits and broad hardening advice with no defect in the change.
- When pull-request discussion is available, inspect it only after the
  independent review. Validate, deduplicate, and attribute sourced findings.

## Output

Return candidate findings first. Use this shape for each one:

```text
[P1] Short imperative title
Confidence: 0.00-1.00
Location: path/to/file.ext:start-end
Impact: What breaks or becomes unsafe
Evidence: The traced path and why existing checks do not prevent it
Fix direction: The smallest credible correction
```

Order findings by priority. Then list checks reviewed and residual risk. If no
issue meets the bar, say `No candidate correctness or security findings.` and
name the most important unverified test gap.
