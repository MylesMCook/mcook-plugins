# Changelog

## 0.2.3 - 2026-11-13

- Describe the adaptation as targeting coding agents generally, not Codex only.

## 0.2.2 - 2026-11-08

- Add an explicit Claude manifest for claude.ai marketplace synchronization.

## 0.2.1 - 2026-08-31

- Remove the repo-specific `desktop-screenshot` skill from the general Buzz
  plugin.
- Restore the focused `buzz-cli` package boundary for everyday relay
  operations.

## 0.2.0 - 2026-08-31

- Add Block's `desktop-screenshot` skill for Buzz desktop UI evidence.
- Scope screenshot capture to a Buzz source checkout and require explicit
  authorization before pushing screenshot branches or commenting on a PR.
- Record the exhaustive upstream skill inventory and retain `buzz-cli` as the
  single copy behind the upstream `sprout-cli` symlinks.

## 0.1.0 - 2026-08-31

- Add the portable `buzz-cli` skill and OpenAI compatibility manifest.
- Adapt Block's Buzz managed-agent guidance for the installed CLI boundary.
- Add explicit external-write authorization and a bounded memory-patch retry.
- Document Buzz output contracts, messaging, agents, repositories, workflows,
  memory operations, pagination, and known limits.
