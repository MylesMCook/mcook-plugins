---
name: claude-code
description: Use when Codex should call the local Claude Code CLI for setup checks, asks, or second opinions.
---

# Claude Code CLI

Read `../../references/claude-cli-contract.md` before running Claude.

Set `HELPER` to this skill's `../../scripts/claude-code.mjs`; run from the target repo.

## Workflow

1. Inspect the repo/request first.
2. Setup: `node "$HELPER" setup`
3. Resolve missing-executable or launch errors before interpreting auth. If Claude
   starts and reports logged out, check sandbox auth using the harness's permitted workflow.
4. Ask: `node "$HELPER" ask -- "<prompt>"`
5. Codex owns edits, checks, and final judgment.

## Guardrails

- Investigate OAuth/keychain access only after Claude starts and reports logged out.
- Do not let Claude edit files through this plugin.
- Do not pass secrets unless explicitly requested.
- Use `--dry-run` before risky external context.
