# Language And Architecture Policy

## Decision

For a new MCP server, default to:

```text
Go server
TypeScript UI only when needed
Remote stateless Streamable HTTP
Portable MCP and MCP Apps metadata
Optional host adapters
```

This default optimizes for a small dependency graph, clear concurrency, fast startup, straightforward operations, and simple binary or container distribution.

## Language selection

Use the first matching rule.

| Situation | Choice |
|---|---|
| Healthy existing server or service | Keep its language unless there is a concrete migration reason |
| New API, database, filesystem, or service integration | Go |
| MCP App with custom UI | Go server plus TypeScript UI |
| Edge runtime or JavaScript-native platform | TypeScript |
| Closest official example is the fastest low-risk path | Adapt that example, then preserve portable contracts |
| Existing Python backend or Python-native workload | Python |
| Existing Rust product, native systems integration, hostile binary parsing, cryptography, or strict memory control | Rust |
| Performance concern without measurements | Go first, benchmark before escalating |

Go and Rust are both official Tier 1 MCP SDKs. Tier status does not erase language tradeoffs. Rust remains an explicit workload choice rather than the ordinary integration-service default.

## Repository shape

Use this for a non-trivial remote server with optional UI:

```text
my-mcp/
|-- cmd/
|   `-- server/
|       `-- main.go
|-- internal/
|   |-- domain/
|   |-- service/
|   |-- adapters/
|   |   |-- mcp/
|   |   `-- upstream/
|   `-- config/
|-- web/
|   |-- src/
|   |-- package.json
|   `-- vite.config.ts
|-- internal/ui/dist/
|-- go.mod
|-- go.sum
|-- README.md
`-- Dockerfile
```

Small servers may start as one Go file. Split only when the code has earned the structure.

## Boundary rules

- Domain and service packages must not depend on MCP SDK types.
- MCP handlers translate between tool schemas and domain inputs or outputs.
- Upstream API clients live behind small interfaces.
- Authentication establishes a principal before a tool handler reaches business logic.
- Durable user state belongs in an external store keyed by the authenticated principal.
- Request-scoped values travel through `context.Context`.
- UI assets are build outputs. Embed them with `go:embed` when a single artifact is useful.
- A host-specific metadata alias must live beside the MCP adapter, not inside domain logic.

## Transport policy

### Remote

Use stateless Streamable HTTP at `/mcp`.

For the pinned official Go SDK `v1.7.0`:

```go
&mcp.StreamableHTTPOptions{Stateless: true}
```

This enables the modern `2026-07-28` path while the SDK can still negotiate supported legacy protocol versions. Do not maintain a separate legacy server unless a real incompatibility requires it.

Do not use MCP session identifiers as database keys or business state keys. Modern MCP requests are independent.

### Local

Use stdio when the server must access the user's machine. Ship a normal executable first. Add MCPB only when a target host and distribution workflow require it.

## MCP App policy

The server can be Go even though the UI is TypeScript.

The Go server owns:

- tool and resource registration
- schemas and annotations
- authentication and authorization
- business state
- `structuredContent`, `content`, and `_meta`
- the `ui://` resource and its security metadata

The TypeScript UI owns:

- rendering
- local interaction state
- MCP Apps bridge calls
- accessibility and responsive behavior
- capability-detected ChatGPT extensions

Use the MCP Apps bridge as the foundation. Treat `window.openai` as an optional extension layer. Do not branch on the host name.

## Release shapes

### Public remote server

Ship one of:

- a small container image
- a platform service deployment
- a self-contained Go binary behind managed HTTPS

Publish:

- stable `/mcp` URL
- auth and privacy documentation
- tool contract and examples
- version and compatibility policy
- operational runbook
- checksums or image digests

### Source release

Include reproducible build commands, pinned modules, tests, and a minimal example client or Inspector script.

### Local package

Build a Go binary per target OS and architecture. Package as MCPB only when needed. A single universal MCPB containing incompatible platform binaries is not automatically portable.

## Host optimization without lock-in

Codex is the preferred authoring environment. ChatGPT is the first product validation target.

That does not change the release contract:

- core tools use standard MCP
- UI uses standard MCP Apps
- OpenAI compatibility aliases are optional
- extensions are capability-detected
- the tool-only path remains useful
- release validation includes another compatible client when broad portability is claimed
