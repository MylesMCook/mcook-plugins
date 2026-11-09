# Changelog

## 0.2.1 - 2026-08-28

- Corrected the safe Git revision example so a validated revision is not
  interpreted as a pathspec.
- Made the TypeScript picker template self-contained and defined its
  idempotency key at the call site.
- Ran optional MCPB signing and verification through the same pinned package
  runner used by the clean-machine workflow.

## 0.2.0 - 2026-08-27

- Changed the greenfield backend default from TypeScript to Go for ordinary MCP integration services.
- Defined Go server plus TypeScript UI as the default MCP App architecture.
- Added explicit rules for portable releases, host adapters, and legacy protocol compatibility.
- Updated the source hierarchy from the former Apps SDK documentation to current MCP, MCP Apps, and OpenAI Plugins documentation.
- Updated remote server guidance for MCP `2026-07-28` and the official Go SDK `v1.7.0`.
- Added portable Agent Plugins metadata and OpenAI skill metadata.
- Corrected MCPB guidance to the current stable `0.3` manifest and made compiled Go binaries the default local package.
- Verified the scaffolds with Go `1.27.0`, Node `26.8.1`, the Go SDK
  `v1.7.0`, `@modelcontextprotocol/ext-apps@1.7.5`, MCPJam `5.2.0`, and
  Codex `0.150.1`.
- Updated MCP Apps examples to the current `toolresult` event API and documented
  compatibility-only resource URI aliases.
- Added the required MCPB `server.mcp_config` block and pinned the verified
  `@anthropic-ai/mcpb@2.1.2` validation commands.
