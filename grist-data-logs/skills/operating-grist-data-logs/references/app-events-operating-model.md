# AppEvents Operating Model

Use Grist as a private, queryable projection of application events. The
application's own durable state remains the source of truth; Grist is neither
the request-path dependency nor a message queue.

## Context and Decision

This model supports a small private application that needs durable operational
history and low-friction analysis, not a high-volume telemetry platform. Its
users are the application owner and the Grist operator. Hard constraints are
private self-hosting, bounded batches, server-side credentials, and no new
always-on service just to move log rows.

The chosen design is a durable application outbox plus a worker that writes
bounded REST batches to Grist. It sacrifices instant analytics during a Grist
outage in exchange for keeping application availability and data ownership in
the application.

Alternatives considered:

- **Synchronous request-path writes:** simplest code, but a Grist outage can
  fail or slow application work; reject for durable operations.
- **Outbox plus bounded REST worker:** recommended. It has one visible retry
  boundary and preserves the app as source of truth.
- **A queue, proxy, or REST-to-MCP bridge:** defer. Each adds a service,
  credential store, and recovery surface without solving a current requirement.

## Boundary

```text
application transaction -> durable outbox -> bounded batch -> Grist AppEvents
                                                        -> receipt + verification
                                                        -> read-only analysis
```

- Generate `EventId` at the producer and never reuse it for a different event.
- Write an event to the application's own durable outbox in the same durable
  unit as the change it describes, where that is practical.
- A worker submits the exact batch through `ingest`. It must retain the input
  until it receives a successful response and records a receipt.
- The helper caps one input file at 1,000,000 bytes and 100 events by default.
  Raise either limit only after measuring the producer, Grist, and recovery
  behavior at the larger size.
- On a timeout or uncertain response, retry the same bytes and event IDs. Do
  not synthesize replacement events during a retry.
- The helper requests Grist's `noupdate` guard. A same-ID replay is retry-safe,
  while a reused ID cannot update a stored row. It is still not exactly-once:
  Grist does not make the `EventId` text column unique, so verification is what
  detects a duplicate or mismatched collision.

Use `--verify` or `verify-ingest` for batches that need a post-write proof.
They check that each submitted ID appears once with the expected six fields,
splitting filtered record reads into conservative URL-safe requests before the
write begins.
Use `--receipt-out` to write a payload-free acknowledgement containing the
batch hash, count, target, and completion time.

## Failure Behavior

| Failure | Producer behavior | Grist behavior |
| --- | --- | --- |
| Connection failure or timeout | Retain batch; retry with a bounded backoff. | State may be unknown; verify before retiring the batch. |
| 429 or 5xx | Retain batch; honor `Retry-After` when available and bound retries. | Do not increase batch size to compensate. |
| 4xx validation or auth failure | Quarantine the batch and alert an operator. | Do not retry unchanged input indefinitely. |
| Duplicate or mismatched ID on verification | Stop that batch and investigate the producer. | Do not overwrite or delete rows to hide it. |
| Grist outage | Continue normal application work where possible; retain the outbox. | Treat analysis as stale until the worker catches up. |

Do not add a new queue, proxy, or REST-to-MCP bridge just for this flow. A
durable application outbox plus bounded REST batches is the smallest useful
failure boundary.

## Compatibility and Ownership

Keep the six-column envelope stable. Add fields only through a reviewed,
additive schema plan; do not rename, retype, or delete current columns. Keep
existing event types readable forever: introduce a new type when meaning
changes and mark the old one deprecated in the producer registry. Treat
`verify-ingest` as a contract test for an existing batch before changing the
helper or a producer.

The producing application owner owns the outbox, event-type registry, payload
redaction, and delivery alerts. The Grist operator owns document access, API
key issuance, backups, and the `grist-mini` recovery runbook. Name a backup
owner before relying on the log for incident analysis.

## Security and Privacy

- Use HTTPS for non-loopback Grist URLs. The helper permits `http://` only for
  `localhost`, `127.0.0.1`, or `::1` development paths.
- Keep the Grist API key server-side and document-scoped. A Community/OSS
  instance uses this REST path; it does not expose the built-in MCP endpoint.
- Exclude credentials, session tokens, raw request/response bodies, payment
  data, and unnecessary personal data from `Payload` before writing an event.
- Treat receipts and helper output as operational metadata. They intentionally
  omit payloads and tokens.

## Observability

Track these at the producer/worker boundary:

- outbox count and age of the oldest unacknowledged batch;
- batch hash, count, attempt count, elapsed time, and delivery outcome;
- authenticated `doctor` failures, repeated 4xx responses, and 429/5xx rate;
- verification failures, missing IDs, duplicate IDs, and mismatched events.

Alert on a growing or aging outbox rather than silently making Grist a hard
dependency for the application.

## Rollout, Rollback, and Recovery

1. Use a dedicated test document and a least-privilege API key.
2. Run `doctor`, create a reviewed additive schema plan, and apply it only
   after explicit approval.
3. Submit one synthetic batch with `--verify --receipt-out`.
4. Replay that exact batch and verify it again.
5. Enable a production worker behind an application feature flag or canary
   source with a small batch limit and monitor outbox age.

Rollback criteria include a growing outbox, repeated verification failures, or
unexpected sensitive data in a payload. To roll back, disable the producer
worker or feature flag and preserve its outbox and receipts. Keep the additive
Grist schema in place. Restore the Grist instance only through the existing
`grist-mini` backup and restore workflow when the document data itself needs
recovery.
