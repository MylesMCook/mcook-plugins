# Changelog

## 0.1.1 - 2026-08-24

- Added the portable Agent Plugins 1.0.0 manifest while retaining the Codex
  compatibility overlay.

## 0.1.0 - 2026-07-10

- Adds an operating model for durable producer outboxes, receipts, verification,
  recovery, privacy, and observability.
- Adds an information model for controlled event types, payload evolution, and
  durable query facets.
- Adds optional payload-free ingestion receipts and post-write verification.
- Prevents a reused `EventId` from overwriting a stored event before
  verification.
- Initial release of a self-hosted Grist event-logging and analysis plugin.
- Adds replay-safe REST ingestion, additive schema planning, read-only SQL,
  and Full-edition MCP guidance.
