# Format Playbook

Use this file when the writing task has a recognizable channel or artifact.

## Documentation

Default structure:

```markdown
# [Task or feature]

[One-sentence outcome: what this helps the reader do.]

## Prerequisites

- [Requirement]
- [Access or dependency]

## Quick start

1. [Action]
2. [Action]
3. [Verification]

## Common options

| Option | Use when | Notes |
|---|---|---|

## Troubleshooting

### [Symptom]

Cause: [likely cause]<br>
Fix: [action]
```

Rules:
- Start with what the reader can accomplish.
- Put the fastest successful path before edge cases.
- Include commands readers can copy.
- Separate concept from procedure.

## README

Minimum useful README:

1. What it is.
2. Who it is for.
3. Install.
4. Quick start.
5. Configuration.
6. Examples.
7. Troubleshooting.
8. Contributing or support.

Avoid vague claims like “simple, powerful, and flexible.” Show a concrete example instead.

## Commit messages

Default:

```text
Imperative subject under about 72 characters

Explain why the change was needed, any tradeoffs, and anything risky.
```

Good subjects:
- `Fix token refresh race`
- `Add retry budget for upload worker`
- `Document SSO setup`

Avoid:
- `Updated stuff`
- `Fixes`
- `Implemented functionality for...`

## Pull request descriptions

Use:

```markdown
## Summary

- [Main change]
- [Main change]

## Why

[Problem, decision, or context.]

## Testing

- [Test command or scenario]
- [Manual verification]

## Risks

[Known risk, migration, rollout note, or “Low: ...”]
```

Add screenshots, logs, or examples when they reduce reviewer effort.

## Release notes

Write for users, not implementers.

Weak:
> Refactored authentication middleware.

Better:
> Login sessions now refresh automatically after temporary network failures.

## Error messages

Formula:

```text
[What happened]. [Why, if known]. [Next action].
```

Examples:
- `We could not save the report because the connection timed out. Try again.`
- `This token expired. Create a new token and rerun the command.`
- `No matching project found for "atlas". Check the project name or run list-projects.`

Avoid blame:
- `Invalid input`
- `You failed to...`

## UI copy

Rules:
- One idea per string.
- Lead with the action.
- Use the user’s words, not internal implementation terms.
- Avoid “please” unless the product voice requires it.
- Avoid “successfully” unless it disambiguates.

Examples:
- `Save changes`
- `Invite teammate`
- `Connection lost. Reconnect to continue.`
- `Delete workspace? This removes all projects and cannot be undone.`

## Emails

Default structure:

```text
[Ask, decision, or answer.]

[Brief context.]

[Next step, owner, and timing.]
```

Example:

```text
Could you review the API handoff by Thursday?

The frontend work starts Friday, and the team needs the final response shapes before then.

The main open question is how we represent partial refunds.
```

## Slack or Teams

Keep it skimmable:
- Lead with the ask or update.
- Use one short paragraph or bullets.
- Name the deadline if there is one.
- Put deep context in a thread or doc.

## Feedback

Use behavior, impact, request:

```text
When [specific behavior], it [specific impact]. Could you [specific request] next time?
```

Example:
> When PRs arrive without test notes, reviewers have to reconstruct the validation path. Could you add a short `Testing` section before requesting review?

## Status updates

Use:

```markdown
Status: [Green/Yellow/Red or plain-language state]

Done:
- ...

Next:
- ...

Blocked/Risks:
- ...

Need:
- ...
```

## Summaries

A good summary is selective. Use:

1. Bottom line.
2. Key evidence or decisions.
3. Open questions or next actions.

Do not preserve the source order if a different order helps the reader.

## Reports

Use an executive summary when the reader needs a decision.

```markdown
## Executive summary

[Decision, recommendation, or key finding.]

## Findings

1. [Finding + evidence]
2. [Finding + evidence]

## Recommendation

[Specific action and rationale.]

## Risks and open questions

- ...
```

## Code comments and docstrings

Write comments for why, invariants, warnings, and non-obvious choices. Do not narrate obvious code.

Weak:
```js
// Increment i by 1
i++;
```

Better:
```js
// Keep the retry count below the provider's rate-limit threshold.
```

## Final answers from an agent

- Answer first.
- Use citations near claims when required.
- Keep bullets short and purposeful.
- Do not add a generic conclusion.
- Offer at most one practical next step unless the user asks for options.
