# Version Pins

Last verified: 2026-08-27.

| Component | Current guidance |
|---|---|
| MCP specification | `2026-07-28` |
| Official Go SDK | Pin `v1.7.0` |
| Go toolchain | Go `1.27.0` verified; Go `1.25` remains the SDK floor |
| Go HTTP option for modern path | `StreamableHTTPOptions{Stateless: true}` |
| MCP Apps browser bridge | `@modelcontextprotocol/ext-apps@1.7.5` |
| MCP Apps frontend toolchain | Node `26.8.1`, TypeScript `7.0.2`, Vite `8.2.2`, `vite-plugin-singlefile@2.3.3` |
| MCP Apps protocol shape | `ui://`, `_meta.ui.resourceUri`, and `text/html;profile=mcp-app` |
| OpenAI product docs | OpenAI Plugins documentation under `/plugins/` |
| MCPB stable manifest | `0.3` |
| MCPB CLI | `@anthropic-ai/mcpb@2.1.2` |
| MCPJam CLI | `@mcpjam/cli@5.2.0` |
| Codex CLI | `0.150.1` |

## Refresh procedure

Before a material release:

1. verify the current MCP specification
2. verify official SDK tiers
3. inspect the pinned Go SDK and MCP Apps releases and migration notes
4. verify the current Go and Node toolchains used by the fixtures
5. verify OpenAI Plugins connection, packaging, UI, and review docs
6. verify both the stable MCPB manifest and current CLI if local packaging is included
7. verify the current MCPJam and Codex CLIs used by validation
8. update this file and the changelog
9. rerun the full compatibility matrix

Do not silently replace dependency pins while changing application behavior.
