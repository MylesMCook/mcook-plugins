# Cici

Ask the local Claude Code CLI for a second opinion, a read-only review, or a fix
plan. Codex owns edits, checks, and final judgment.

Cici carries forward the three skills and helper from Claude Code 0.1.0.
It replaces Claude Code Advisor without bringing over its orchestration layer.

- `$cici:claude-code`: setup checks, questions, and second opinions.
- `$cici:claude-code-review`: read-only code review.
- `$cici:claude-code-rescue`: investigation help and a minimal fix plan.

Requires Node.js and an existing authenticated `claude` CLI on PATH. Cici does
not install Claude, change authentication, or choose a model for you. The helper
retains the original command-line behavior and uses Claude's configured default.

Run from the target repository. Each skill resolves the bundled
`scripts/claude-code.mjs` helper relative to its own location. Use `--dry-run` to
inspect prompts and `--no-git-context` until sharing diff context is approved.
Claude runs with tools disabled and plan permissions; Codex applies any fixes.

## Install

After the marketplace release:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add cici@mcook-plugins-local
```

Verify Cici is installed before removing the old `claude-code-advisor` and
`claude-code` installations. Start a new chat to load the Cici skill namespace.

## Verify

```sh
node --test cici/tests/*.test.mjs
node cici/scripts/claude-code.mjs ask --dry-run -- "Explain this API boundary."
```

On Windows, the helper resolves `claude.exe` on PATH or the native executable
inside npm's adjacent `node_modules/@anthropic-ai/claude-code/bin` directory.
It skips shell and batch shims and passes prompts directly without a shell.
Unix executable lookup is unchanged. Setup reports launch errors separately
from authentication failures; an unsupported shim-only installation is reported
as a missing supported executable.
