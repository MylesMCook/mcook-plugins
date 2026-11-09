# assistant-ui

An original documentation routing skill plus the official assistant-ui hosted
MCP. It helps with setup, components, runtimes, tools, streaming, persistence,
and upgrades while following the project's existing choices.

## Use

Install from Myles Codex Plugins:

```sh
codex plugin add assistant-ui@mcook-plugins-local
```

Start a new chat, then try:

- "Use $assistant-ui to explain the runtime options for my existing backend."
- "Debug why this @assistant-ui thread stops updating."
- "Find the official migration guide for the versions in this lockfile."

The package contains one skill, `assistant-ui`. Upstream `/setup`, `/runtime`,
and other skills are read directly from GitHub as needed, not copied into the
package or registered as additional commands. Each new task checks the current
upstream index and reads the relevant guide and supporting references, using
one commit where possible. Upstream content updates need no plugin release or
scheduled sync. This requires network access; if GitHub is unavailable, the
skill falls back to official documentation and reports the gap.
There are no hooks, automatic installers, or application dependencies.

## Sources and connection

- [Official AI documentation guide](https://www.assistant-ui.com/docs/llm)
- [Documentation index](https://www.assistant-ui.com/llms.txt)
- [Complete documentation](https://www.assistant-ui.com/llms-full.txt)
- [Upstream skills](https://github.com/assistant-ui/skills)
- [Source and releases](https://github.com/assistant-ui/assistant-ui)

`mcp.json` connects directly to `https://www.assistant-ui.com/mcp` using
Streamable HTTP. No local MCP process or API key is configured. The service
requires network access and is operated by assistant-ui. If unavailable, the
skill uses the documentation index and individual `.md` pages through an
available web tool.

The remote service provides documentation, examples, and template discovery;
its `preview_template` tool creates a hosted preview. The skill requires that
remote action to be authorized and excludes secrets and private project data
from queries and previews. Merely installing this package does not create a
preview or an Assistant Cloud account.

Portable Agent Plugins 1.0.0 packaging includes an OpenAI compatibility
manifest. The Claude catalog supplies its equivalent HTTP MCP configuration.
MCP protocol target: current/legacy compatibility; the observed handshake uses
`2025-03-26`. This is not a claim of MCP `2026-07-28` conformance.

## Provenance and validation

This is a Myles Cook integration, not an official assistant-ui plugin. The
skill is original; it links to upstream content without redistributing the
upstream skills. The `assistant-ui/skills` README and Claude plugin manifest
declare MIT (checked 2026-10-09), although GitHub's repository license metadata
is empty. The main `assistant-ui/assistant-ui` repository also declares MIT.
Linked material remains subject to its own license.

See [verification](tests/verification.md) for checks and limitations.
