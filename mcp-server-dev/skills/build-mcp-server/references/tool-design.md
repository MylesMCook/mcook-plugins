# Tool Design

Tool names, descriptions, schemas, and annotations are part of the runtime contract. They affect discovery, selection, confirmation, retries, and client UI.

## One Job Per Tool

Each tool should represent one atomic user job. Split reads from writes and separate discovery from exact-ID operations.

Good:

```text
search_issues
get_issue
create_issue
close_issue
```

Bad:

```text
manage_issues
```

Use standard `search` and `fetch` shapes when the server is connector-like, knowledge-oriented, or meant to participate in broad retrieval workflows.

## Names And Descriptions

Use stable action-oriented names. Begin descriptions with a behavioral cue:

```text
Search issues by keyword across title and body.
Use this when the user does not already know the issue ID.
Does not search comments or pull requests.
```

State:

- what the tool does
- when to use it
- when not to use it
- which sibling tool should be called first or next
- whether it reads, creates, updates, deletes, or reaches an external system

Do not depend on server-level instructions to repair vague tool descriptions.

## JSON Schemas

Use JSON Schema Draft 2020-12 unless the selected SDK documents a different requirement.

Tighten every schema with the constraints the domain already knows:

- descriptions for every property
- `required`
- enums for closed sets
- integer versus number
- minimum and maximum bounds
- string length or format constraints
- defaults only when the server applies them consistently
- `additionalProperties: false` for closed input objects
- an output schema when structured results are stable

Do not make SDK-specific schema syntax the architecture. Zod, Go structs, Rust types, or Python models are implementation details that must compile to the same wire contract.

## Annotations

Set all relevant hints explicitly and accurately.

| Annotation | Meaning |
|---|---|
| `readOnlyHint` | The tool does not modify its environment. |
| `destructiveHint` | The tool may delete, overwrite, revoke, or otherwise perform a change that is difficult to undo. This matters only for non-read-only tools. |
| `idempotentHint` | Repeating the same call with the same arguments has no additional effect. This matters only for non-read-only tools. |
| `openWorldHint` | The tool may interact with external entities or an unbounded external environment. `false` means the interaction stays inside a bounded, closed domain. |

Hints must describe actual behavior. They are not a security boundary and do not replace authorization or confirmation.

## Result Contract

Return deliberately separated channels:

- `content`: concise model-readable narration or fallback
- `structuredContent`: stable reusable data matching the output schema
- `_meta`: UI-only or host-specific data that should not enter model context
- `isError`: recoverable domain or tool failure that the model can see and correct

Prefer IDs, canonical URLs, timestamps, next actions, and bounded lists. Avoid raw HTML, giant upstream payloads, secrets, stack traces, and meaningless `ok` responses.

A useful error explains recovery:

```json
{
  "isError": true,
  "content": [
    {
      "type": "text",
      "text": "Item itm_404 was not found. Use search_items to discover a valid ID."
    }
  ]
}
```

Protocol failures are for malformed or unsupported protocol operations. Expected upstream and domain failures belong in visible tool results.

## Retry And Mutation Policy

For every write tool decide:

- whether retries are safe
- whether the upstream supports an idempotency key
- what object version or precondition prevents lost updates
- whether explicit user confirmation is required
- what the tool returns after a duplicate request

Do not mark a create operation idempotent unless the implementation actually deduplicates repeated calls.

## Surface Size

Prefer a small stable catalog. When a large upstream API would create dozens of overlapping tools, use a deliberate search-plus-execute or hybrid surface rather than exposing the upstream mechanically.

Do not hide materially different permissions or destructive behavior behind one generic executor merely to reduce tool count.

## Review Checklist

Before release, verify:

- names are stable and unambiguous
- sibling descriptions do not overlap
- schemas reject malformed and extra input
- output schemas match actual structured results
- annotations match behavior
- writes have authorization, retry, and confirmation policy
- errors provide a recoverable next step
- result size is bounded
- every tool remains useful without custom UI
