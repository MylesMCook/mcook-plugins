---
name: goalie
description: Use when the user wants to turn a rough idea, dirty goal, messy long-run prompt, sidechat thought, or under-scoped Codex task into clean Goal objective text under 4000 characters. Produce ready-to-use Goal text without the `/goal` prefix. Do not use for normal one-off prompts, ordinary implementation plans, brainstorming with no intended Codex Goal, or starting a Goal unless explicitly asked.
---

# Goalie

Turn rough intent into clean Goal objective text for Codex.

## Core Rule

Default output is draft-only Goal text.
- Do not include `/goal`.
- Keep the Goal objective text under 4000 characters.
- Do not call Goal tools or start a Goal unless the user explicitly asks in the current request.
- Prefer one strong Goal over a menu of options.
- If the task is too small or too vague for a Goal, say so and give a better normal prompt or the next clarifying question.

## Goal Fit Test

Use a Goal when the work has:
- a durable objective that may take multiple turns
- a finish line Codex can audit with evidence
- a path that may change after investigation

Do not use a Goal for:
- one-line edits
- simple explanations
- short reviews
- normal plans that stop after one answer
- vague requests with no meaningful evidence source

## Workflow

1. Extract the user's actual target:
- desired end state
- why this needs a longer Codex run
- likely workspace, repo, file, artifact, test, benchmark, source, or evidence surface
- realistic verification environment when the result depends on deploys, devices, data, flags, auth, browsers, or external systems
- whether visual material is context, evidence, or the actual finish line

2. Build the completion contract:
- Outcome: what must be true when done
- Evidence: tests, benchmark, report, artifact, command output, source material, or runtime check that proves it
- Environment: the real or production-like surface Codex should use to verify the result; if unavailable, state the limitation
- Progress tracking: for long goals, milestone commits, a status artifact, draft PR, or update cadence
- Constraints: what must not regress or be changed
- Boundaries: allowed files, tools, repos, data, time, or scope limits
- Iteration policy: how Codex should choose the next action between attempts
- Visual guardrails: for visual goals, prefer feature checklists, design-system adherence, accessibility, and real UI inspection over pure pixel matching; forbid fake matches such as cropping or inlining a reference image
- Finalization: review the final diff/artifacts, remove failed experiments, rerun relevant checks, and report residual risk
- Blocked stop: when Codex should stop and report the real blocker, attempts already made, smallest unblock action, and who or what can unlock progress

3. Ask only for missing critical details. If a reasonable default exists, use it and list it under `Assumptions`.

4. Draft the Goal as compact objective text the user can paste after `/goal`.

5. Self-check before final output:
- no `/goal` prefix
- Goal objective text is under 4000 characters
- no fake certainty
- no broad "make it better" wording
- includes evidence and constraints when available
- includes environment, progress tracking, visual guardrails, and finalization when they affect success
- says what to report if blocked
- does not claim completion, build success, test success, deployment, device behavior, or production readiness unless verified

## Current-Thread Goal Starts

If the user explicitly asks to start a Goal in the current thread, first produce the cleaned Goal text and confirm it has a real evidence surface. Only then use the host's Goal tool if available and allowed by the current environment.

If the Goal becomes genuinely blocked, use the Goal tool's blocked state only after the same blocking condition has repeated for the required Goal-turn threshold. Do not mark a Goal blocked merely because the work is hard, slow, uncertain, or would benefit from clarification.

## Writing Standard

Goal text should be clear and compressed, not exhaustive.
- Lead with the desired end state.
- Use concrete nouns, direct verbs, and parallel clauses.
- Cut filler, backstory, repeated caveats, and process narration.
- Put secondary context in `Why this works` or `Assumptions`, not inside the Goal.
- If the draft approaches 4000 characters, shorten it before returning it.

## Output Shape

Use this format:

```text
Goal:
[ready-to-use Goal objective text, no /goal prefix]

Why this works:
- Outcome: ...
- Evidence: ...
- Environment: ...
- Progress tracking: ...
- Constraints: ...
- Boundaries: ...
- Iteration policy: ...
- Visual guardrails: ...
- Finalization: ...
- Blocked stop: ...

Assumptions:
- ...

Optional sharper version:
[alternate Goal objective text, no /goal prefix]
```

Omit non-applicable `Why this works` lines except `Outcome`, `Evidence`, and `Blocked stop`.
Omit `Optional sharper version` unless it gives a materially better tradeoff.

If the prompt is not Goal-worthy, use this format:

```text
This should be a normal prompt, not a Goal:
[better one-off prompt or concise reason]
```

## Failure Modes

- Including `/goal` even though the user wants to add it themselves.
- Returning Goal objective text at or above 4000 characters.
- Starting a Goal when the user only asked for draft text.
- Turning normal planning into a Goal.
- Omitting verification, constraints, or blocker handling.
- Marking a Goal complete without evidence.
- Marking a Goal blocked before the required repeated-blocker threshold.
- Asking broad intake questions instead of making safe assumptions.
