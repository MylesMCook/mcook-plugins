---
name: claude-code-rescue
description: Use when Codex should ask Claude Code CLI for investigation help or a fix plan while Codex keeps edit control.
---

# Claude Code Rescue

Read `../../references/claude-cli-contract.md` before running Claude.

Set `HELPER` to this skill's `../../scripts/claude-code.mjs`; run from the target repo.

## Workflow

1. State the failure and desired outcome.
2. Preview with `node "$HELPER" rescue --dry-run -- "<problem>"` if external context is sensitive.
3. Run `node "$HELPER" rescue -- "<problem>"`
4. If auth is hidden by the sandbox, rerun with shell escalation.
5. Convert useful advice into Codex-owned edits.
6. Report what was verified.

## Guardrails

- Claude proposes; Codex executes.
- Do not delegate remote side effects.
- If Claude suggests broad refactors, narrow them before acting.
- Use `--no-git-context` unless sending diff context is approved.
