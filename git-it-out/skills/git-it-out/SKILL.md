---
name: git-it-out
description: "Complete final repository closeout when the user explicitly asks to git it out, get it out, ship completed work, or otherwise hand off a substantially finished session. Inspect repository state, run required gates, create proper commits, land and push mainline, and complete only configured release, deployment, tracker, checkpoint, and cleanup steps. Do not use for implementation, open-ended debugging, release planning, or casual statements that do not clearly authorize closeout."
---

# Git It Out

Use this skill when the work is substantially complete and the user wants the agent to own the remaining closeout all the way to the repo's final landing point.

## Boundaries

- Use it for final last-mile closure: verification, proper commits, main/mainline landing, push, release, deploy, publish, tracker, checkpoint, and handoff work.
- Do not use it for greenfield implementation, broad refactors, deep debugging, or release-process design from scratch.
- If you discover the work is not actually closeable yet, clear only the blockers required to reach the intended finish line, then stop expanding scope.

## Authorization

- Skill activation is not authorization for external or destructive actions.
- A direct request such as "git it out," "ship this completed work," or "take this from here and finish it" authorizes the repository's normal documented closeout path.
- "I'm done" or "I'm going to bed" counts only when paired with clear takeover or closeout language. Do not infer authorization from those statements alone.
- When activation is implicit without a direct closeout request, perform only read-only inspection and safe local validation. Ask once before pushing, merging, releasing, deploying, publishing, modifying trackers, or deleting branches.

## Load `references/finish-checklist.md` when

- the user says "git it out," "get it out," or clearly wants final no-dangling-session closeout,
- the finish line touches more than one surface, such as main plus tracker plus deploy,
- an irreversible action is about to happen,
- repo policy or branch protection adds gates you must satisfy, or
- you need a completion checklist before handing back status.

## Default Stance

- Treat a direct closeout request as ownership transfer for the repository's documented final path. Do not infer that transfer from a casual statement of fatigue or completion alone.
- Infer the intended landing path from repo instructions, branch or PR state, CI signals, release config, deployment config, and task context before asking questions.
- Prefer the repo's native path over generic Git habits.
- Treat repo-native checkpoint, release, or closeout tooling such as Entire as first-class only when it is actually configured.
- Default to the smallest complete path that leaves the work landed, pushed, and cleaned up at the repo's real final surface.
- Use branches or PRs only as mechanisms when the repo requires them; do not treat an open PR or pushed branch as final done unless a hard external gate blocks merging or landing.
- Ask only when the irreversible target is ambiguous, credentials or authority are missing, verification reveals a production-impacting blocker, or repo or user policy requires approval.

## Closeout Procedure

1. Inspect the state: git status, active branch, pending diffs, PR or review state, CI, release or deploy config, and task context.
2. Determine the actual finish line: proper commit(s), main/mainline landing, push, release, deploy, publish, production verification, or handoff-ready partial completion because of an external blocker.
3. Identify required gates for that finish line: tests, lint, build, typecheck, approvals, changelog or release notes, tracker state, migrations, feature flags, checkpoint capture, or other repo-native checks.
4. Run the last useful validation for the chosen finish line and fix only finish-blocking issues. Re-run until the gate passes or you hit a true blocker.
5. Create proper commit(s), land or merge them to the repo's final mainline surface, and push the result.
6. Execute repo-native release, deploy, publish, production verification, tracker, checkpoint, and handoff steps in order.
7. Clean up every surface that is part of done: PR, branch, tracker, release artifact, deploy surface, checkpoints, and handoff notes.
8. Report the final state clearly, including anything that could not be completed.

## Ask vs Act

- Keep moving through the documented closeout path when the user directly requested final closure and the target is clear.
- If activation was implicit rather than directly requested, stop before external, shared, production-visible, or destructive actions and ask once for confirmation.
- Ask when the destination, authority, credentials, production target, or repository policy is unclear.
- If an external system blocks the last step, complete everything up to that blocker and leave a precise handoff.

## Guardrails

- Do not invent a release or deployment process.
- Do not treat "finish the session" as permission to bypass required review, CI, release, or production gates.
- Do not leave a branch or PR as the final state when the repo permits landing to main/mainline.
- Do not assume Git usage alone means Entire is active.
- Do not broaden scope into unrelated cleanup or quality polish.
- Do not both merge and deploy unless the workflow actually requires both.
- Do not leave branch, tracker, release, or handoff cleanup half-done when it is part of the finish line.
- Do not hide skipped checks, failed gates, residual risk, or manual follow-up.

## Output

- What landed.
- Where it landed.
- What was verified.
- Which surfaces were updated.
- Whether the repo is clean and pushed.
- Any residual risk, remaining blocker, or next follow-up.
