---
name: thermos
description: >-
  Run Thermos when the user asks for Thermos, both thermo-nuclear review lenses,
  a paired or double review, parallel correctness and maintainability review,
  or a review-fix-review loop until Thermos is happy. Resolve one change scope,
  run two independent native review subagents in parallel, verify
  their findings, and return one prioritized review.
---

# Thermos

Run one correctness and security review beside one maintainability review. Keep
both reviewers independent until the parent verifies and combines their work.

## Native subagents

Thermos uses exactly two native review-only children, one per lens. Inspect the
actual spawn surface; use available host defaults unless the user selects a
supported route. Task names are labels, not proof of model or reviewer identity.
Do not install agent profiles or assume a particular runtime tool signature.

For explicitly adversarial or three-reviewer work, use the sibling
[adversarial-review](../adversarial-review/SKILL.md) workflow instead. Do not run
both entrypoints for one request.

## Boundaries

- Default to a read-only review. Do not edit files, stage changes, post review
  comments, push, or create external side effects.
- Use a single sibling skill when the user asks for only one review lens.
- Do not use Thermos for an ordinary quick review or a full-repository security
  scan. Route the latter to a security-scanning workflow.
- Enter the repair loop only when the user explicitly asks to fix findings,
  iterate, or work until Thermos is happy.

## Load both rubrics

Before delegation, resolve these paths relative to this `SKILL.md` and read
them completely:

- [Correctness and security rubric](../thermo-nuclear-review/SKILL.md)
- [Maintainability rubric](../thermo-nuclear-code-quality-review/SKILL.md)
- [Subagent contract](references/subagent-contract.md)

Pass each reviewer the exact resolved sibling path and require it to read that
file. Do not rely on an unqualified same-name skill when legacy copies may also
be installed. If a reviewer cannot load the file, stop and report an
installation or discovery problem.

## Resolve and verify one scope

Read [the shared review contract](references/review-contract.md) before spawning.
Use it to establish scope and later verify and synthesize the findings.

## Run the paired review

1. Use the host's native subagent-spawn tool to start exactly two review-only
   children in the same wave. Do not simulate either review in the parent.
   When the current tool exposes `fork_turns`, set it to `"none"` and pass the
   compact scope contract instead of the parent transcript.
2. Give both the same scope contract, not a pasted full repository dump. Give
   each only its matching rubric path and role contract from
   `references/subagent-contract.md`.
3. Tell each reviewer to inspect the scoped checkout independently, avoid
   nested delegation, and return only candidate findings, checks, and residual
   risk. Never let either reviewer synthesize a verdict or make a change.
4. Wait for both reviewers before synthesis. If two parallel children cannot
   start, report that Thermos could not run its paired workflow; do not replace
   it with a sequential surrogate.

Child threads inherit the parent permission mode. Retain the no-write
instruction and verify the scope identity before and after all required reviews. When
read-only enforcement matters, select a read-only parent permission mode before
asking Thermos to delegate.

## Explicit repair loop

When the user explicitly authorizes fixes:

1. Let the parent fix only verified findings and run the narrowest relevant
   checks.
2. Capture a new scope identity.
3. Spawn a fresh same-wave pair of review-only reviewers with the same
   contracts. Do not ask the old pair to grade its own advice.
4. Repeat until no verified `P0`, `P1`, or `P2` findings remain, or a real
   blocker requires user input.

Do not broaden the requested change while chasing reviewer preferences.

## Output

- State the reviewed scope and excluded dirty state.
- State that the two native child threads ran, or why the paired workflow could
  not start.
- Lead with verified findings, ordered by priority.
- List checks run or inspected and any remaining test gap.
- End with `patch is correct` or `patch is incorrect`, a concise explanation,
  and an overall confidence score from `0` to `1`. A verified `P0`, `P1`, or
  `P2` makes the patch incorrect. `P3` notes alone do not.
- If no finding survives verification, say so directly. Do not pad the answer
  with generic praise or repeat both reviewer summaries.
