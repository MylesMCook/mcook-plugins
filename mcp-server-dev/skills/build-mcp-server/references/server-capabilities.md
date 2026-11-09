# Server Capabilities

## Core primitives

Prefer tools, resources, and prompts before optional protocol features.

Use server instructions for a small amount of cross-tool routing guidance that cannot fit in one tool description.

## MCP 2026-07-28

Modern requests are self-contained and do not require an initialization handshake or transport session.

Relevant modern features include:

- `server/discover`
- per-request capability metadata
- deterministic and cacheable list results
- `resultType`
- multi-round-trip requests with `inputRequests`, `inputResponses`, and `requestState`
- formal extensions

Implement only the features the workflow needs.

## Multi-round-trip input

For a tool that requires user input or another client-provided response:

- return an input-required result
- include exact input requests
- include opaque `requestState`
- validate the echoed state on retry
- encrypt and authenticate state for unauthenticated servers
- keep a non-interactive fallback when practical

Use [elicitation.md](./elicitation.md).

## Deprecated core features

Roots, sampling, and protocol logging are deprecated in MCP `2026-07-28`.

Do not add them to a new architecture unless legacy client support or a specific migration requires them. Isolate legacy use and document the removal plan.

Use normal application logs and observability instead of MCP protocol logging.

## Cancellation and deadlines

- honor `context.Context`
- propagate safe deadlines upstream
- stop work after cancellation
- make writes retry-safe or explicitly non-idempotent
- avoid background work that outlives the request unless represented by a durable task or job

## Capability rule

For every optional capability or extension:

- negotiate or inspect support
- provide a fallback
- test a supported and unsupported client
- do not infer support from a product name
