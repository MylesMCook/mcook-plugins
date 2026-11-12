# Changelog

## 0.2.5 - 2026-11-12

- Document Cursor, Claude, and Factory Droid catalog wiring, including root `.mcp.json` and `droids/` copies that Droid needs.

## 0.2.4 - 2026-11-08

- Add an explicit Claude manifest for claude.ai marketplace synchronization.

## 0.2.3 - 2026-10-10

- Require Agent Plugins conformance before release, with validation evidence for the exact release candidate.
- Require explicit native-only exception documentation covering the client limitation, compatibility limits, reproducible evidence, native checks, and the condition for reconsidering portability.

## 0.2.2 — 2026-10-04

- Validate safe pinned external Git catalog sources alongside contained local entries.
- Add metadata-only entry validation without claiming portable-package validation.
- Add cross-platform synthetic regression coverage and document isolated-install migration checks.


## 0.2.1 - 2026-08-27

- Accept Codex's versioned `<plugin>/<version>/` installed-cache layout during
  portable package validation while retaining strict source-directory identity
  checks.
- Add installed-cache coverage and document direct validation of installed
  package bytes.

## 0.2.0 - 2026-08-07

- Added portable Agent Plugins 1.0.0 as an explicit package target with canonical root manifests and fixed component discovery.
- Added bundled canonical schemas and an `uv`-native validator for schema, path, MCP transport, secret, OpenAI overlay, and marketplace conformance.
- Added a portable-plus-OpenAI target and migrated the builder package itself to that layout.
- Added an explicit MCP 2026-07-28 compatibility gate covering Codex opt-in, discovery, stateless metadata, multi-round input, pagination, caching, subscriptions, and deprecations.
- Removed machine-specific validation paths in favor of active skill roots and cross-platform `uv run` commands.

## 0.1.1 - 2026-07-27

- Aligned package guidance with the current OpenAI plugin architecture and public-submission boundary.
- Added focused skill-activation coverage and forward-compatible app-component validation guidance.
- Replaced the retired plugin documentation link.

## 0.1.0 - 2026-07-10

- Added the initial repo-native Codex plugin creation workflow.
- Added marketplace registration, validation, provenance, and publication guidance.
