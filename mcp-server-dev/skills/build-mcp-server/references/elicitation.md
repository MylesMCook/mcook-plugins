# User Input And Elicitation

MCP `2026-07-28` replaces server-initiated session callbacks with multi-round-trip request results.

## Use it for

- short confirmations
- small flat forms
- one or two constrained choices
- required client input that cannot be inferred safely

## Do not use it for

- searchable collections
- rich layouts
- nested editors
- visual previews
- long-lived dashboards

Those cases belong in `build-mcp-app`.

## Modern flow

1. The tool returns `resultType: input_required`.
2. The result includes one or more `inputRequests`.
3. The result includes opaque `requestState`.
4. The client fulfills the requests.
5. The client retries the tool with `inputResponses` and the same `requestState`.
6. The server validates state and completes or requests another round.

The exact Go SDK API is version-sensitive. Read the pinned SDK documentation before implementing it.

## State security

`requestState` crosses an untrusted boundary.

- bind it to the operation and principal
- expire it
- sign or encrypt it
- reject replay where replay is unsafe
- never put secrets or raw credentials in it
- do not assume transport affinity

## Confirmation

A confirmation is not authorization.

Before a destructive action:

- authenticate the principal
- authorize the exact resource and action
- return precise impact information
- obtain confirmation through a supported input or UI flow
- use an idempotency key when duplicate execution is possible

## Fallback

When a client lacks the required input flow, return a clear model-readable result explaining what information is required and how to retry. Do not silently guess.
