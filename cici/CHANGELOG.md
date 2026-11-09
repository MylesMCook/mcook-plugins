# Changelog

## 0.1.1 - 2026-10-15

- Resolve native Windows Claude executables, including the npm installation,
  without executing shell shims or interpreting prompt text in a shell.
- Report process launch failures separately from authentication and return a
  numeric failure exit code for ask, review, and rescue.
- Add executable discovery and argument-boundary regression tests.

## 0.1.0 - 2026-10-12

- Transfer the three Claude Code 0.1.0 skills, CLI helper, contract, and tests
  unchanged into Cici.
- Add portable metadata, Codex compatibility metadata, and skill discovery labels.
- Replace the Advisor workflow with direct, read-only Claude CLI calls.
