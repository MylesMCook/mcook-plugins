---
name: build-mcp-server
description: Build, refactor, review, or release an MCP server; choose Go, TypeScript, Python, or Rust; define tools and schemas; select remote HTTP or local stdio; design auth; add optional MCP Apps UI; or validate MCP 2026-07-28 and client portability.
---

# Build An MCP Server

This is the front door for MCP server work.

The default greenfield architecture is a Go server using the official Go SDK,
stateless Streamable HTTP at `/mcp`, and TypeScript only for optional MCP App
UI. The current verified baseline is Go `1.27.0` with the SDK pinned to
`v1.7.0`; keep Go `1.25` as the minimum SDK floor when broader build-toolchain
compatibility matters.

Do not replace a healthy existing stack merely to follow the default.

## Sources

Read these first:

1. [SOURCE-OF-TRUTH.md](../../SOURCE-OF-TRUTH.md)
2. [LANGUAGE-AND-ARCHITECTURE.md](../../LANGUAGE-AND-ARCHITECTURE.md)
3. [CLIENT-VALIDATION-PLAYBOOK.md](../../CLIENT-VALIDATION-PLAYBOOK.md)

For current product behavior, fetch the live documentation before making version-sensitive claims.

## Workflow

### 1. Inspect the current state

Before proposing code:

- inspect the repository, nearest `AGENTS.md`, dependency files, transport, auth, tools, tests, deployment, and release process
- identify the actual target clients
- identify whether this is greenfield, an extension, or a migration
- preserve working architecture unless a concrete defect or constraint justifies change
- state what was inspected and what remains unverified

### 2. Classify the server

Choose one primary shape.

| Shape | Use when |
|---|---|
| Remote tool-only | Shared API, database, or service integration without custom UI |
| Remote MCP App | Shared server plus inline UI |
| Local stdio | Filesystem, desktop app, localhost, or OS integration |
| Local MCPB | A target host needs one-file local installation |
| Hybrid | A shared remote core plus a separate local adapter is genuinely required |

Do not use MCPB for a normal cloud integration.

### 3. Plan tools before code

For every tool define:

- one user job
- action-oriented name
- title and a description beginning with `Use this when...`
- exact input and output schemas
- required fields, enums, bounds, defaults, and `additionalProperties`
- `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint`
- authorization requirement
- retry behavior
- model-readable `content`
- reusable `structuredContent`
- optional UI-only `_meta`
- whether UI materially improves the job

Prefer a small stable surface. Split reads from writes. Use standard `search` and `fetch` shapes when the server is connector-like or intended for knowledge retrieval.

Use [tool-design.md](references/tool-design.md).

### 4. Choose the language

Use the first matching rule:

1. Keep the language of a healthy existing service.
2. Use Go for a new ordinary integration server.
3. Use Go plus TypeScript for a new MCP App.
4. Use TypeScript for JavaScript-native edge runtimes, Workers, or a clearly superior official example. For Cloudflare Workers, follow [deploy-cloudflare-workers.md](references/deploy-cloudflare-workers.md).
5. Use Python for an existing Python backend or Python-native workload.
6. Use Rust for an existing Rust system, native or FFI work, hostile binary parsing, cryptography, or measured memory and latency constraints.

Do not choose Rust merely for theoretical performance. Do not choose TypeScript merely because OpenAI examples use it.

### 5. Choose transport and protocol behavior

#### Remote default

- Streamable HTTP
- stable `/mcp` endpoint
- public HTTPS for public release
- stateless request handling
- modern MCP `2026-07-28`
- SDK-negotiated legacy compatibility when required

For the pinned Go SDK `v1.7.0`, set:

```go
&mcp.StreamableHTTPOptions{Stateless: true}
```

Do not use MCP session identifiers for business state. Store durable state by authenticated principal in an external store.

#### Local default

Use stdio. Build a normal executable. Package as MCPB only when the target distribution requires it.

### 6. Establish boundaries

Keep these layers separate:

```text
domain
service
upstream adapters
MCP adapter
HTTP or stdio transport
optional UI build
```

Domain and service packages must not import MCP SDK types.

Put authentication middleware before MCP handling. Put authorization inside the service boundary or immediately before service calls. Keep secrets outside source control.

### 7. Implement the smallest complete slice

Start with:

- one representative tool
- health endpoint for remote servers
- typed input and output
- useful text result
- structured result
- error mapping
- unit test
- protocol-level test

Use [remote-http-scaffold.md](references/remote-http-scaffold.md) for a Go remote baseline.

Add tools only after the first slice passes.

### 8. Add authentication deliberately

Use [auth.md](references/auth.md).

Rules:

- authenticate the request before business logic
- validate issuer, audience, scopes, and expiry
- never forward the incoming MCP bearer token to another service
- use token exchange or service-owned credentials upstream
- key durable state by principal, not transport session
- keep public and private data paths explicit

### 9. Add UI only after the tool works

Hand off to `build-mcp-app` when inline UI adds real value.

The tool-only path must remain useful. The server can remain Go while the UI is TypeScript.

### 10. Validate before release

Use the full validation playbook.

At minimum:

- format, compile, unit tests, and integration tests
- modern `2026-07-28` request path
- every legacy version claimed
- schemas, annotations, structured results, errors, and auth
- ChatGPT developer-mode evaluation
- another client when broad portability is claimed
- clean-checkout build and documented release artifact

Do not claim protocol support from process startup or a successful legacy `initialize` alone.

### 11. Release

Use [portable-release-checklist.md](references/portable-release-checklist.md).

Prefer:

- pinned Go modules
- reproducible build
- small container or self-contained binary
- stable HTTPS endpoint
- versioned tool contract
- changelog
- checksums or image digest
- explicit compatibility matrix
- host-specific limitations documented separately

## Hard rules

- No host-name branching when capability detection is possible.
- No custom UI as the only useful result.
- No session-bound business state for modern remote MCP.
- No vague or kitchen-sink tools.
- No destructive behavior hidden behind read-like names.
- No generated scaffold called complete until checks actually ran.
- No architecture rewrite solely to satisfy an unverified convenience-host quirk.
- No claim that Go or Rust is required by MCP. They are language choices.

## Output order

When implementing or reviewing, report:

1. inspected state
2. chosen server shape and language
3. tool plan
4. architecture and transport
5. files changed
6. implementation
7. validation run
8. release instructions
9. unverified items or known client limits

For direct implementation requests, do not stop at a plan. Make the changes and run the available checks.
