# Changelog

## 0.1.2 - 2026-11-15

- Align with act v0.2.97: untrusted project `.actrc`, `--container-options-policy`,
  `--validate`, and the current unsupported-feature list.
- Flag installs older than v0.2.92 as missing upstream security fixes.
- Make the README host-neutral with Codex, Claude Code, Factory Droid, and Cursor
  install steps.

## 0.1.1 - 2026-11-08

- Add an explicit Claude manifest for claude.ai marketplace synchronization.

## 0.1.0 - 2026-10-10

- Add one implicitly discoverable skill for local GitHub Actions validation.
- Discover the current installation, config paths, and runtime on each invocation.
- Inspect execution chains, credentials, architecture, and resource requirements.
- Separate permission and setup failures from workflow failures and hosted CI.
- Package portable and OpenAI manifests for the Codex, Cursor, and Claude catalogs.
