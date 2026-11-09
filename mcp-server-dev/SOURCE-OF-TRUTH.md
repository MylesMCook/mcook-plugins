# Source Of Truth

Use this hierarchy whenever implementation guidance conflicts.

## 1. MCP wire protocol

The MCP specification controls transport, methods, schemas, capability negotiation, authorization requirements, and version behavior.

- [MCP 2026-07-28 specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP 2026-07-28 documentation](https://modelcontextprotocol.io/docs/2026-07-28)
- [Official SDK list and tiers](https://modelcontextprotocol.io/docs/2026-07-28/sdk)
- [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)

For Go:

- [Official Go SDK documentation](https://go.sdk.modelcontextprotocol.io/)
- [Official Go SDK repository](https://github.com/modelcontextprotocol/go-sdk)
- [Go SDK rough edges](https://go.sdk.modelcontextprotocol.io/rough_edges/)

Default version floor for new Go projects:

- Go `1.25` or newer
- `github.com/modelcontextprotocol/go-sdk` pinned to `v1.7.0`
- `StreamableHTTPOptions{Stateless: true}` for the modern `2026-07-28` HTTP path

The current verified authoring toolchain is Go `1.27.0`. Pin exact dependency
versions in released repositories. Refresh the pins deliberately instead of
following `main`.

## 2. MCP Apps extension

MCP Apps controls portable in-chat UI behavior.

- [MCP Apps overview](https://modelcontextprotocol.io/extensions/apps/overview)
- [Build an MCP App](https://modelcontextprotocol.io/extensions/apps/build)
- [MCP Apps API documentation](https://apps.extensions.modelcontextprotocol.io/)
- [MCP Apps source and examples](https://github.com/modelcontextprotocol/ext-apps)

Portable UI requirements:

- `ui://` resource URI
- `text/html;profile=mcp-app`
- `_meta.ui.resourceUri`
- JSON-RPC over the MCP Apps bridge
- narrow `_meta.ui.csp`
- useful tool-only fallback

The current verified browser bridge is `@modelcontextprotocol/ext-apps@1.7.5`.
Use `app.addEventListener("toolresult", handler)`; the older
`app.ontoolresult` callback is deprecated. Some hosts still require the flat
`_meta["ui/resourceUri"]` key. Keep `_meta.ui.resourceUri` authoritative and
add the flat key only as a compatibility alias when an actual host test needs
it.

## 3. OpenAI product integration

OpenAI Plugins documentation controls ChatGPT and Codex packaging, testing, product-specific metadata, optional extensions, and submission.

- [Combined OpenAI Plugins documentation](https://developers.openai.com/plugins/llms-full.txt)
- [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins)
- [MCP server concept](https://developers.openai.com/plugins/concepts/mcp-server)
- [Brainstorm use cases](https://developers.openai.com/plugins/plan/use-case)
- [Define tools](https://developers.openai.com/plugins/plan/tools)
- [Build an MCP server](https://developers.openai.com/plugins/build/mcp-server)
- [Add UI](https://developers.openai.com/plugins/build/chatgpt-ui)
- [Authentication](https://developers.openai.com/plugins/build/auth)
- [Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [Connect and test](https://developers.openai.com/plugins/deploy/connect-chatgpt)
- [Optimize metadata](https://developers.openai.com/plugins/guides/optimize-metadata)
- [Security and privacy](https://developers.openai.com/plugins/guides/security-privacy)
- [Troubleshooting](https://developers.openai.com/plugins/deploy/troubleshooting)
- [MCP server review requirements](https://developers.openai.com/plugins/deploy/app-review)
- [Plugin reference](https://developers.openai.com/plugins/reference)

OpenAI examples currently emphasize TypeScript and Python. Treat them as product-contract examples, not as a requirement to use those backend languages. Implement the same MCP contract in Go unless another stack is clearly better.

## 4. Local packaging

MCPB is a host-oriented local distribution format, not the universal release format for remote MCP servers.

- [MCPB repository](https://github.com/modelcontextprotocol/mcpb)
- [Current MCPB manifest specification](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md)

Use the current stable manifest version stated by the official MCPB repository. Do not infer a stable version from draft fields or old Anthropic paths.

The current verified CLI is `@anthropic-ai/mcpb@2.1.2`. Manifest `0.3` requires
`server.mcp_config` in addition to `server.type` and `server.entry_point`.

## 5. Secondary clients

Use current documentation from the actual client only after the shared MCP contract is correct.

A host-specific workaround must be:

- isolated behind metadata or a small adapter
- capability-detected where possible
- optional for the core tool path
- covered by a host-specific test

Do not redesign the shared server around an unverified client quirk.
