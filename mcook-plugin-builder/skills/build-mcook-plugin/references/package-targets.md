# Package targets

Choose the package target before choosing files. Agent Plugins and OpenAI-native plugins share components, but they do not share a manifest contract.

## Portable Agent Plugin 1.0.0

Use this target when skills or MCP servers should load across compatible clients.

```text
plugin-name/
├── plugin.json
├── skills/
│   └── skill-name/
│       └── SKILL.md
├── mcp.json
└── com.example.client/
```

- Require root `plugin.json` with `$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`.
- Discover only immediate `skills/*/SKILL.md` children and root `mcp.json`.
- Do not put component paths in `plugin.json`; locations are fixed.
- Require root `mcp.json` to use `$schema: https://agent-plugins.org/schemas/1.0.0/mcp.schema.json`.
- Put client-specific manifest data under `extensions.<reverse-domain-name>` and client-specific files under a same-named root directory.
- Keep all package-resolved paths inside the plugin root. Avoid symlinks for Codex installation compatibility.
- Treat Agent Plugins 1.0.0 as a working-draft contract pinned by its canonical schemas.

Agent Plugins v1 defines only Agent Skills and MCP servers as portable components. Hooks, apps, commands, agents, rules, UI, installation, and publication remain client-owned.

## OpenAI-native plugin

Use this target only when a concrete client limitation or required capability prevents a conforming portable core with client extensions. Before release, satisfy the [native-only exception requirements](../SKILL.md#release-deliberately). OpenAI apps, hooks, or legacy compatibility do not by themselves justify omitting the portable core.

```text
plugin-name/
├── .codex-plugin/plugin.json
├── skills/
├── .mcp.json
├── .app.json
└── hooks/hooks.json
```

- Keep the OpenAI manifest at `.codex-plugin/plugin.json`.
- Use `.mcp.json`, `.app.json`, and `hooks/` only when those components are real.
- Follow current OpenAI documentation and its validator. Do not infer public-submission acceptance from portable-schema validation.

## Portable core plus OpenAI compatibility

Use this repository default for a new or materially revised plugin whose skills or MCP servers are portable but whose marketplace presentation or compatibility remains OpenAI-specific.

```text
plugin-name/
├── plugin.json
├── .codex-plugin/plugin.json
├── skills/
├── mcp.json
└── optional OpenAI-only files
```

- Make root `plugin.json` authoritative for portable identity and metadata.
- Put Codex interface data under `extensions.com.openai` in root `plugin.json`.
- Keep `.codex-plugin/plugin.json` as a legacy OpenAI compatibility manifest; its `name` and `version` must match the portable manifest.
- Keep portable components at their fixed locations. The OpenAI overlay must not redirect `skills/` or `mcp.json`.
- Add `.mcp.json` only when pre-portable Codex compatibility is an explicit requirement. If both MCP files exist, generate them from one reviewed server definition or compare them in tests so they cannot drift.
- Describe this honestly as a portable core with an OpenAI compatibility layer, not a pure vendor-neutral package.

Codex 0.147.0 reads `extensions.com.openai` first and otherwise can use `.codex-plugin/plugin.json` as a compatibility overlay for interface, apps, and hooks. Other Agent Plugins clients ignore that OpenAI data.

## Independent MCP protocol target

Package format does not select MCP wire protocol. For each bundled or remote server, separately record one of:

- legacy/current-default compatibility;
- MCP `2026-07-28` only; or
- dual-protocol support.

Read [mcp-2026-07-28.md](mcp-2026-07-28.md) whenever a server targets the 2026 protocol or the request mentions the July 2026 MCP changes.

## Source baseline

Verified 2026-08-07 against the [Agent Plugins 1.0.0 specification](https://agent-plugins.org/specification), [portable manifest contract](https://agent-plugins.org/plugin-authors/manifest), [portable MCP configuration](https://agent-plugins.org/plugin-authors/mcp-servers), [OpenAI package documentation](https://developers.openai.com/plugins/build/plugins), [Codex 0.147.0 release notes](https://learn.chatgpt.com/docs/changelog#month-2026-08), and the [Codex portable-plugin implementation](https://github.com/openai/codex/pull/36544).
