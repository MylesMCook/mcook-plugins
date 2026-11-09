# Host Compatibility

Build the shared MCP contract first. Add host behavior only after the standard path passes.

## Layers

### Standard core

- MCP tools, resources, prompts, and auth
- supported protocol versions
- Streamable HTTP or stdio
- MCP Apps `_meta.ui.resourceUri`
- `text/html;profile=mcp-app`
- MCP Apps bridge
- text and structured fallbacks

### OpenAI adapter

- `.codex-plugin/plugin.json`
- ChatGPT developer-mode connection
- optional `openai/outputTemplate`
- optional `window.openai` capabilities
- OpenAI submission metadata

### Other host adapters

Add only documented metadata or behavior required by a named target client.

## Rules

- Capability-detect instead of checking product names.
- Keep aliases additive.
- Do not place host-specific types in domain or service packages.
- Test every adapter in the host it targets.
- Document the tested host version and date.
- Remove stale workarounds when the host implements the standard path.
- Do not market untested clients as supported.

A client failing to render optional UI is not proof that the tool contract is broken. A tool contract failing protocol tests is not a client quirk.
