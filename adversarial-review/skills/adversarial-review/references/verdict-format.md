# Verdict Format

## Verdict: PASS | CONTESTED | REJECT

<one-line summary>

## Findings

<numbered list ordered by severity: high -> medium -> low, or `No material findings.`>

For each finding include:

- **[severity]** Description with file:line references
- Reviewer: which Codex subagent raised it
- Lens: which reviewer lens raised it
- Evidence: what concrete code path, diff hunk, or failure scenario supports it
- Recommendation: concrete action, not vague advice
- Lead judgment: accept | reject - one-line rationale

Reject or demote any finding that lacks concrete evidence.

## Next Action

<the smallest concrete action that resolves accepted findings, or "None">

## Coverage

When all reviewers succeed, use one line:

`Skeptic, Architect, Minimalist: success`

Only expand per-reviewer coverage when there is a failure or evidence gap. When
applicable, name the exact failure class:

- `SUBAGENT_UNAVAILABLE`
- `SUBAGENT_FAILED`
- `TIMEOUT`
- `MALFORMED_OUTPUT`
- `INCOMPLETE_COVERAGE`
- `NO_REVIEWABLE_TARGET`

## Verdict Logic

- **PASS** - all three reviewers completed and no accepted high-severity
  findings remain; accepted medium or low findings may remain as non-blocking
  recommendations
- **CONTESTED** - coverage is incomplete, a high-severity claim remains
  materially disputed, or evidence is too thin to clear the change
- **REJECT** - at least one accepted high-severity finding blocks ship
