---
name: operating-grist-data-logs
description: Operate self-hosted Grist as a replay-safe application event log. Use for AppEvents schemas, REST logging, read-only SQL analysis, Grist API credentials, or deciding whether self-hosted Grist MCP is appropriate.
license: MIT
---

# Operating Grist Data Logs

Use Grist as a document-scoped event store with a small, explicit boundary:

```text
application server -> Grist REST API -> AppEvents document/table
                                      -> read-only SQL analysis
                                      -> optional interactive MCP analysis
```

Use REST for application writes. Use read-only SQL for deterministic analysis.
Use MCP only for interactive work after the user accepts that data returned to
an AI client is visible to that client's AI provider.

## Non-negotiable rules

- Keep `GRIST_TOKEN` server-side. Never place an API key in browser code,
  client-side configuration, sample data, generated artifacts, or command
  output.
- Use a dedicated, document-scoped service account where the Grist edition and
  installation support it. Grant only the logging document and only the
  required scopes.
- Treat `EventId` as an immutable producer ID. Ingestion uses Grist's
  `noupdate` guard, so a reused ID cannot overwrite a stored event. Verification
  distinguishes an exact replay from a collision; never reuse an ID for a
  different event.
- Run only one parameterized `SELECT` or `WITH ... SELECT` statement for
  analysis. Do not use raw SQLite access to a running Grist document.
- `apply-schema` and `ingest` modify a live document. Show the exact command,
  target URL, document ID, table, and batch source, then wait for explicit
  approval before running either command.
- Do not enable MCP, OIDC, public ingress, or change a persistent Grist
  service without approval. These are instance configuration changes, not
  plugin setup.

## Design the Log

Before wiring a producer, read
[app-events-operating-model.md](references/app-events-operating-model.md) and
[app-events-information-model.md](references/app-events-information-model.md).
They establish the source-of-truth boundary, outbox and recovery behavior,
event vocabulary, payload evolution, and findability model. Keep the current
six-column envelope until evidence supports an additive field.

## Normal workflow

1. Confirm the target is a self-hosted Grist instance and determine whether it
   is Community or Full edition. Community supports the REST workflow; the
   built-in MCP endpoint requires Full edition.
2. Define the producer's event-type registry and durable outbox contract. Grist
   is a projection for analysis, not the application's source of truth.
3. Configure `GRIST_URL`, `GRIST_DOC_ID`, and `GRIST_TOKEN` in the application
   server's existing secret-management path. Do not put them in a tracked
   `.env` file.
4. Run `doctor` to verify authenticated document access and inspect table IDs.
5. Run `plan-schema --table AppEvents`. Review its additive plan and any type
   conflicts. A plan never changes Grist.
6. After approval, run `apply-schema` with the exact table confirmation. It
   rejects edited or stale plans, non-additive changes, and type conflicts.
7. Validate JSON or JSONL events offline, then after approval run `ingest` with
   `--verify --receipt-out`. Retain the exact input until verification and a
   receipt succeed.
8. Prefer `query` for analysis when an API key is available. It permits a
   single read-only statement with separately encoded arguments and no trailing
   semicolon; Grist's SQL endpoint does not accept OAuth tokens.

The bundled helper is at `scripts/grist_ops.py`:

```sh
export GRIST_URL="https://grist.internal.example"
export GRIST_DOC_ID="document-id"
export GRIST_TOKEN="from-your-secret-manager"

python3 scripts/grist_ops.py --pretty doctor
python3 scripts/grist_ops.py --pretty plan-schema --table AppEvents --out /tmp/app-events-plan.json
python3 scripts/grist_ops.py --pretty apply-schema --plan /tmp/app-events-plan.json --confirm-table AppEvents
python3 scripts/grist_ops.py --pretty ingest --table AppEvents --input events.jsonl --verify --receipt-out /tmp/app-events-receipt.json
python3 scripts/grist_ops.py --pretty verify-ingest --table AppEvents --input events.jsonl
python3 scripts/grist_ops.py --pretty query --sql 'SELECT EventType, count(*) AS count FROM AppEvents GROUP BY EventType'
```

## Event contract

`ingest` accepts a JSON array or JSONL. Each object must include an event ID,
timestamp, and event type using either camel case or snake case:

```json
{
  "event_id": "01J9E8FQSGXZE2K8C5NM7X0Q1W",
  "occurred_at": "2026-07-10T15:04:05Z",
  "event_type": "run.completed",
  "payload": {"duration_ms": 183}
}
```

`source` and `environment` can be supplied per event, as command options, or
by `GRIST_LOG_SOURCE` and `GRIST_LOG_ENVIRONMENT`. Payloads are stored as
canonical JSON text so the write contract remains stable and portable. For a
controlled event taxonomy and payload-evolution rule, use
[app-events-information-model.md](references/app-events-information-model.md).

## MCP decision

For a Full self-hosted instance, the built-in MCP endpoint is
`https://<grist-host>/api/mcp`. An API-key MCP client needs
`GRIST_MCP_ENABLED=true`. ChatGPT, Claude, and similar interactive clients
also require `GRIST_ENABLE_OIDC_SERVER=true` and a deliberately restricted
`GRIST_OIDC_CIMD_ALLOWED_HOSTS` list, such as `chatgpt.com`.

Do not bundle an unofficial REST-to-MCP bridge. It adds another hosted service,
token store, write surface, and prompt-injection boundary without improving the
REST logging workflow. On Community edition, continue with REST plus the
read-only SQL endpoint.

Read [references/grist-sources.md](references/grist-sources.md) before making
decisions that depend on Grist capabilities or endpoint behavior.
