# Grist Data Logs

`grist-data-logs` is a Codex plugin for using self-hosted Grist as a bounded
application event log and analysis store.

It packages one skill, `operating-grist-data-logs`, and a standard-library
helper at `scripts/grist_ops.py`.

## What it does

- Plans and applies an additive `AppEvents` table schema with stale-plan,
  edited-plan, and type-conflict protection.
- Validates a JSON or JSONL batch and adds rows using producer-generated
  `EventId` values. Exact retries are safe, while a reused ID cannot overwrite
  an existing event.
- Runs one parameterized, read-only `SELECT` or `WITH` SQL query through the
  documented Grist API.
- Explains the correct self-hosted MCP path without treating Community edition
  as if it exposed the built-in MCP endpoint.

## Design Contract

Grist is a queryable projection of application events, not the application's
source of truth or request-path dependency. The recommended shape is a durable
application outbox, bounded REST batches, a payload-free receipt, and optional
post-write verification.

Read the [operating model](skills/operating-grist-data-logs/references/app-events-operating-model.md)
before wiring a producer and the [information model](skills/operating-grist-data-logs/references/app-events-information-model.md)
before defining event types. They keep the six-column envelope small while
giving event names, payloads, privacy, recovery, and analysis a durable shape.

## Configuration

Keep these values in the existing server-side secret-management mechanism:

```sh
export GRIST_URL="https://grist.internal.example"
export GRIST_DOC_ID="document-id"
export GRIST_TOKEN="api-key-or-scoped-oauth-token"
export GRIST_LOG_SOURCE="application-name"
export GRIST_LOG_ENVIRONMENT="production"
```

Run the helper from this plugin root:

```sh
python3 scripts/grist_ops.py --pretty doctor
python3 scripts/grist_ops.py --pretty plan-schema --table AppEvents --out /tmp/app-events-plan.json
# Apply only after reviewing the plan and approving the target document/table.
python3 scripts/grist_ops.py --pretty apply-schema --plan /tmp/app-events-plan.json --confirm-table AppEvents
python3 scripts/grist_ops.py --pretty ingest --input events.jsonl --verify --receipt-out /tmp/app-events-receipt.json
python3 scripts/grist_ops.py --pretty verify-ingest --input events.jsonl
python3 scripts/grist_ops.py --pretty query --sql 'SELECT EventType, count(*) AS count FROM AppEvents GROUP BY EventType'
python3 scripts/grist_ops.py --pretty mcp-info --edition community
```

`ingest` and `verify-ingest` accept at most 100 events and 1,000,000 input
bytes by default. Tune `--batch-size` or `--max-input-bytes` only after a
measured producer and recovery test.

`doctor`, schema operations, ingestion, and `verify-ingest` support a scoped
OAuth token or API key. `query` uses Grist's API-key-only SQL endpoint, so use
an API key for that command.

## MCP

Self-hosted built-in MCP requires the Full edition. Its endpoint is
`https://<grist-host>/api/mcp`. An API-key client needs
`GRIST_MCP_ENABLED=true`; interactive clients such as ChatGPT also require
the built-in OIDC server and a deliberate CIMD allowlist. Those settings alter
a persistent service and are intentionally guidance-only here.

MCP analysis is not automatically private from the AI provider. Treat a
connector as access for that provider to any rows it reads or writes.

`EventId` is retry-safe for an exact replay, not a database-enforced unique
constraint. Ingestion uses Grist's `noupdate` guard, so a reused ID cannot
overwrite an existing event; `--verify` then detects missing, duplicate, and
mismatched rows. Verification splits its filtered reads before the write, so a
batch cannot be accepted and then fail solely because the verification URL is
too long.

## Verification

```sh
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/grist_ops.py
```

## Sources

See [Grist sources](skills/operating-grist-data-logs/references/grist-sources.md).

## License

MIT. See [LICENSE](LICENSE).
