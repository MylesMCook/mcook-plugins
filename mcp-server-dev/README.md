# mcp-server-dev

Skills for designing, building, validating, and releasing portable MCP servers and MCP Apps from Codex.

## Default architecture

| Concern | Default |
|---|---|
| Backend | Go with the official `modelcontextprotocol/go-sdk` |
| Remote transport | Stateless Streamable HTTP at `/mcp` |
| UI | TypeScript, only when inline UI materially improves the workflow |
| MCP App integration | Standard MCP Apps bridge first |
| ChatGPT behavior | Optional capability-detected extensions |
| Local-machine distribution | Stdio server, optionally packaged as MCPB |
| Validation | Protocol checks, ChatGPT, then at least one secondary client when portability matters |

The released server core is client-neutral. Codex is the primary authoring environment and ChatGPT is the primary product validation target, but neither is allowed to define the wire protocol or domain architecture.

## Skills

| Skill | Purpose |
|---|---|
| `build-mcp-server` | Front door for transport, language, tool design, auth, implementation, validation, and release decisions. |
| `build-mcp-app` | Adds a TypeScript MCP App UI to a working server while preserving a useful tool-only path. |
| `build-mcpb` | Packages a true local-machine stdio server. Defaults compiled Go servers to platform-specific binary bundles. |

## Core rules

- Prefer Go for a new I/O-bound MCP server.
- Prefer the existing language when extending a healthy codebase.
- Use Rust when the workload or existing system specifically benefits from it.
- Use TypeScript end to end when the deployment platform, upstream example, or team stack makes it clearly simpler.
- Keep domain logic independent of MCP SDK request and response types.
- Do not store business state in MCP transport sessions.
- Keep every tool useful without custom UI.
- Treat MCP Apps and host-specific features as additive capabilities.
- Validate the modern `2026-07-28` path and the legacy path you claim to support.

## Start here

1. Read [SOURCE-OF-TRUTH.md](./SOURCE-OF-TRUTH.md).
2. Read [LANGUAGE-AND-ARCHITECTURE.md](./LANGUAGE-AND-ARCHITECTURE.md).
3. Use `build-mcp-server` for every new server or material server refactor.
4. Hand off to `build-mcp-app` only after the tool contract works without UI.
5. Use [CLIENT-VALIDATION-PLAYBOOK.md](./CLIENT-VALIDATION-PLAYBOOK.md) before release.

This plugin is packaged as a portable Agent Plugin with an OpenAI overlay so the same skill core remains usable outside one host.
