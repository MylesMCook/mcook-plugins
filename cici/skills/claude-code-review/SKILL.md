---
name: claude-code-review
description: Use when Codex should ask Claude Code CLI for a read-only review of a diff, branch, or working tree.
---

# Claude Code Review

Read `../../references/claude-cli-contract.md` before running Claude.

Set `HELPER` to this skill's `../../scripts/claude-code.mjs`; run from the target repo.

## Workflow

1. Inspect current git state.
2. Preview with `node "$HELPER" review --dry-run -- "<review focus>"` if external context is sensitive.
3. Run `node "$HELPER" review -- "<review focus>"`
4. If auth is hidden by the sandbox, rerun with shell escalation.
5. Treat Claude output as review input, not truth.
6. Verify accepted findings locally.

## Guardrails

- Keep the review read-only.
- Prioritize bugs, security, regressions, and missing tests.
- If context is truncated, say so.
- Use `--no-git-context` unless sending diff context is approved.
