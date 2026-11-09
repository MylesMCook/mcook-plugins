# AppEvents Information Model

Keep the base `AppEvents` envelope small. It supports known-item lookup,
time-based review, and faceted analysis without turning this general plugin
into an application-specific event registry.

## Canonical Fields

| Field | Required | Meaning and rule |
| --- | --- | --- |
| `EventId` | Yes | Opaque producer-generated ID. It never encodes business meaning and must never be reused for a different event. |
| `OccurredAt` | Yes | Source occurrence time in RFC 3339 with a timezone. Producers should emit UTC; the helper preserves valid timestamp text for replay compatibility. It is not ingestion time. |
| `Source` | Yes | Controlled producer or service slug, such as `web-app` or `sync-worker`; never a person, host name, or secret. |
| `Environment` | Yes | Controlled deployment value, such as `development`, `test`, `staging`, or `production`. Choose one vocabulary and keep it stable. |
| `EventType` | Yes | Controlled lowercase `noun.past-tense-action` term, such as `run.completed` or `run.failed`. |
| `Payload` | Yes | Canonical JSON with only the detail needed for the event's purpose. Never use it as an unbounded request dump. |

The helper does not enforce an application-specific taxonomy. Keep that
governance beside the producing application, where it has an owner and tests.

## Rationale and Tradeoffs

The primary organization model is an event entity with time and independent
facets. `Source`, `Environment`, and `OccurredAt` support broad investigation;
`EventType` narrows to a behavior; `EventId` supports a known-item lookup.
Keeping changing details in `Payload` avoids speculative columns and preserves
the source event's provenance. The tradeoff is that a frequently used payload
key eventually needs an additive column to become an efficient facet.

The field definitions and API boundary are derived from the
[Grist sources](grist-sources.md). The producer-owned registry is the source
of truth for application-specific vocabulary and payload requirements.

## Event Type Registry

Create one small registry in the producer repository. Add a row before a new
event type begins producing in a durable environment.

| Event type | Intent | Producer | Required payload keys | Sensitive-data rule | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `run.completed` | A run reached its successful terminal state. | `sync-worker` | `schema_version`, `duration_ms` | No user content. | Application owner | Active |
| `run.failed` | A run reached a failed terminal state. | `sync-worker` | `schema_version`, `error_code` | Error messages must be redacted. | Application owner | Active |

Add a new type when meaning changes. Deprecate old types but never rename or
reuse them in historical rows. Keep `schema_version` in a payload whenever its
shape evolves; readers can then interpret historical records intentionally.

## Findability

The primary facets are `Source`, `Environment`, and `OccurredAt`. Add
`EventType` when narrowing to a behavior. `EventId` is the direct path for a
known event.

Useful parameterized queries include:

```sql
SELECT OccurredAt, Source, EventType, Payload
FROM AppEvents
WHERE Environment = ? AND EventType LIKE ?
ORDER BY OccurredAt DESC
LIMIT 50
```

Arguments: `["production", "%.failed"]`.

```sql
SELECT EventType, count(*) AS events
FROM AppEvents
WHERE OccurredAt >= ?
GROUP BY EventType
ORDER BY events DESC
```

Arguments: `["2026-07-01T00:00:00Z"]`.

```sql
SELECT EventId, OccurredAt, Source, Environment, EventType, Payload
FROM AppEvents
WHERE EventId = ?
```

Arguments: `["known-event-id"]`.

## Evolution Rule

Start with a payload key. Promote it to a top-level Grist column only after it
becomes a repeated filter, grouping, or join requirement and its type is
stable. Use the additive schema-plan workflow for that promotion; do not
rewrite old payloads to make a new idea look as though it always existed.

Review the registry whenever a new source appears, a payload schema changes,
or a query becomes difficult to answer from the existing facets.

## Open Questions and Validation

Before a production writer is enabled, resolve these for the producing
application:

- Who owns the event registry and approves a new event type?
- Which `Source` and `Environment` values are allowed in the first release?
- Which payload keys are sensitive, and what redaction happens before outbox
  persistence?
- What query must the first dashboard or incident investigation answer?

Validate the model with a synthetic batch: find one known `EventId`, filter
the same records by source and environment, group the events by type, and
place one new event type in the registry without inventing a new category.
