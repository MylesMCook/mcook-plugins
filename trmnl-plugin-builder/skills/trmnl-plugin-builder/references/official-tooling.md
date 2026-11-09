# Official TRMNL agent tooling

Prefer TRMNL's maintained tools over bundled copies or local replacements.

| Need | Official tool |
| --- | --- |
| Agent instructions and design guidance | [`usetrmnl/trmnl-agent-skills`](https://github.com/usetrmnl/trmnl-agent-skills), especially the `trmnl` skill |
| Hosted plugin operations and design-system lookup | TRMNL's hosted MCP at `https://trmnl.com/mcp` with the current authentication method documented by TRMNL |
| Local preview, lint, PNG build, pull, and push | [`trmnlp`](https://github.com/usetrmnl/trmnlp) |
| Product and API documentation | [TRMNL `llms.txt`](https://docs.trmnl.com/go/llms.txt) and its linked pages |
| Framework source and releases | [`usetrmnl/trmnl-framework`](https://github.com/usetrmnl/trmnl-framework) and the live [Framework docs](https://trmnl.com/framework/docs) |

TRMNL currently publishes a native Cursor plugin and a Claude Code plugin in
its agent-skills repository. For Codex, install the official `trmnl` skill from
that source and configure the hosted MCP separately. Do not describe the Codex
skill distribution as an official TRMNL Codex plugin unless TRMNL publishes an
actual Codex-compatible plugin manifest.

Keep this companion thin. Do not copy TRMNL's template guide, Framework guide,
design-system references, tool catalog, or agent prompt into this package.

Use a local preview MCP only for capabilities that official `trmnlp` and the
hosted MCP do not supply. A legacy custom pilot MCP is not a default dependency.
