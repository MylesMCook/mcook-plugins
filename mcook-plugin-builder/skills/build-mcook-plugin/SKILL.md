---
name: build-mcook-plugin
description: >-
  Builds, ports, updates, or reviews plugins for the Myles Codex Plugins
  marketplace, including portable Agent Plugins 1.0.0 packages, OpenAI-native
  plugin packages, dual-format compatibility, and MCP 2026-07-28 readiness.
  Use when creating a reusable marketplace plugin or skill, adapting an external
  plugin, adding portable plugin.json or mcp.json files, reviewing MCP protocol
  compatibility, or preparing a plugin for validation and private release.
---

# Build a Myles Codex plugin

Build the smallest installable package that makes a reusable workflow easier to discover and apply. Keep one-off constraints in the task or `AGENTS.md`; use a skill for reusable procedure; package it when it belongs in this marketplace.

## Select both targets

1. Inspect `AGENTS.md`, `.agents/plugins/marketplace.json`, the existing package, and the closest comparable plugin.
2. Choose the package target before changing files:
   - **Portable** — Agent Plugins 1.0.0 root `plugin.json`, fixed `skills/`, and optional root `mcp.json`.
   - **OpenAI-native** — `.codex-plugin/plugin.json` and optional `.mcp.json`, `.app.json`, or hooks.
   - **Portable plus OpenAI** — portable core with `extensions.com.openai` and the OpenAI compatibility files actually needed.
3. Choose the MCP protocol target separately for every server: default/legacy, `2026-07-28`, or dual-protocol. Package format never proves wire-protocol compatibility.
4. Read [package-targets.md](references/package-targets.md) before creating or migrating manifests. Read [mcp-2026-07-28.md](references/mcp-2026-07-28.md) when the request mentions the July 2026 protocol or a server claims modern compatibility.

Require Agent Plugins conformance for releases in this marketplace. Use a portable core plus OpenAI compatibility when the reusable components are Agent Skills or MCP servers. Select or retain an OpenAI-native-only package only through the documented exception in the [release gate](#release-deliberately), including during a narrow fix.

## Establish the component boundary

1. Use skills only when existing tools suffice; add MCP only for controlled tools, authentication, state, or external services; add UI only when people must inspect, compare, edit, confirm, or navigate structured information. Keep MCP workflows usable without UI.
2. Treat Agent Plugins v1 skills and MCP servers as the only portable components. Put hooks, apps, interface behavior, commands, agents, and rules in an honest client-specific layer.
3. Use `$plugin-creator` for the current OpenAI manifest and ingestion contract. Use `$openai-docs` for current Codex behavior, OpenAI packaging, or publication. Resolve those skill roots from the active catalog; never hard-code a home directory.
4. If a plugin needs a ChatGPT Apps SDK MCP server or widget, invoke `$build-chatgpt-app` with `$openai-docs`. For public submission, use `$chatgpt-app-submission` after implementation. Those workflows do not replace portable or marketplace validation.
5. When adapting upstream work, verify its current source and license. Preserve required attribution and rewrite host-specific behavior rather than copying blindly.

## Build the package

Place the package at the repository root. A portable-plus-OpenAI package normally looks like:

```text
plugin-name/
├── plugin.json
├── .codex-plugin/plugin.json
├── skills/skill-name/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── mcp.json
├── README.md
├── CHANGELOG.md
└── LICENSE
```

- Use the same stable identity and SemVer version in both manifests. This repository defaults to lowercase kebab-case names even though Agent Plugins also permits periods.
- Keep portable component locations fixed. Do not add `skills` or `mcpServers` paths to root `plugin.json`.
- Require canonical Agent Plugins 1.0.0 `$schema` identifiers in root `plugin.json` and `mcp.json`. Keep their specification versions matched.
- Put Codex interface data under `extensions.com.openai`. Keep `.codex-plugin/plugin.json` for this marketplace's OpenAI compatibility; do not let it override portable identity or component locations.
- For portable stdio MCP, use one `command` token and separate `args`. Prefer `uv` for Python packages, `${PLUGIN_ROOT}` for bundled read-only files, and `${PLUGIN_DATA}` for virtual environments, caches, generated content, and other writable state. Do not embed credentials in `env` or headers.
- Add `.mcp.json` only for explicit pre-portable OpenAI compatibility. Add `.app.json` or hooks only for real OpenAI-specific behavior.
- Give each `SKILL.md` concise frontmatter with precise triggers. State inputs, workflow, result shape, and facts the agent must not infer. Keep the body procedural and under 500 lines.
- Generate `agents/openai.yaml` from the completed skill with skill-creator. Declare only real MCP dependencies.
- Write a user-facing README and changelog at the plugin root. Add `ATTRIBUTION.md` only when external material requires it.

## Register it in this marketplace

The canonical catalog is `.agents/plugins/marketplace.json`. Append one entry without reordering existing plugins:

```json
{
  "name": "plugin-name",
  "source": {
    "source": "local",
    "path": "./plugin-name"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Developer Tools"
}
```

The local source path is relative to the marketplace root, not the JSON file, and must remain inside that root. Preserve the catalog name and display name. For reviewed external packages, use the documented `git-subdir` or repository-root `url` source with a credential-free HTTPS GitHub repository URL and exactly one full 40-character commit `ref` or `sha`. Do not copy an external native package merely to make it portable. Validate catalog metadata with `uv run <builder-skill-root>/scripts/validate_agent_plugin.py --marketplace-entry <name> --marketplace .agents/plugins/marketplace.json --marketplace-root .`; this mode never fetches or executes the package and does not validate its contents. Separately inspect the pinned source and verify a fresh isolated installation, manifest/discovery, licenses and installed-byte identity before migrating a live installation. Keep Codex-to-Claude advisor packages out of the Claude catalog.

## Validate before handoff

Resolve `<builder-skill-root>`, `<skill-creator-root>`, and `<plugin-creator-root>` from the active skill catalog. Run only the checks applicable to the chosen targets:

```text
uv run <builder-skill-root>/scripts/validate_agent_plugin.py plugin-name --marketplace .agents/plugins/marketplace.json --marketplace-root . --require-openai-overlay
uv run --with pyyaml==6.0.3 <skill-creator-root>/scripts/quick_validate.py plugin-name/skills/skill-name
uv run --with pyyaml==6.0.3 <plugin-creator-root>/scripts/validate_plugin.py plugin-name
git diff --check
git status --short
```

- Run the bundled Agent Plugins validator for portable or dual packages. Omit `--require-openai-overlay` for portable-only packages.
- Pass a versioned installed cache as the plugin root when validating installed bytes. The validator accepts both `<name>/` source packages and Codex's `<name>/<version>/` cache layout; marketplace mapping arguments apply only to source packages.
- Run the current OpenAI validator for OpenAI-native or dual packages. Treat it as an ingestion check, not Agent Plugins conformance.
- Validate every skill, manifest, declared component, marketplace mapping, package path, and schema. Review warnings instead of waving at them from across the room.
- Test skill activation with direct, indirect, incomplete, nearby non-trigger, and safety/edge cases.
- For MCP, test the actual declared transport, authentication, tools, dependencies, and failure isolation. Use the modern verification gate before claiming MCP `2026-07-28`.
- Finish with a fresh installation/task check when installation is requested. Do not claim publication, installation, or protocol support without observing the live target.

## Release deliberately

Before any release, satisfy one of these two paths and record the validation commands and results for the exact release candidate:

1. **Conforming package:** verify the package against the targeted [Agent Plugins specification](https://agent-plugins.org/specification) and run the bundled portable validator plus the applicable skill, client, marketplace, and runtime checks above. The specification text is authoritative if it conflicts with a schema. Validation errors or unresolved warnings block release; passing an OpenAI ingestion check alone does not satisfy this gate.
2. **Native-only exception:** add a `Native-only exception` section to the plugin README before release. For an external package, use repository-owned documentation linked from its marketplace documentation. Record the concrete client limitation or required capability that prevents a conforming package, why a portable core plus client extensions is insufficient, affected components and supported clients, tested client versions, and reproducible evidence with expected and observed behavior. Record the native validation and runtime checks that pass, their material gaps, and the condition for reconsidering portability. Existing native packaging, convenience, or a failing portable check alone is insufficient justification. Label the package native-only and make no Agent Plugins conformance claim.

An undocumented or unsupported exception blocks release. A native-only exception does not waive applicable skill, client, marketplace, security, or runtime checks, or authorize release actions.

- A Git-backed marketplace release is not public ChatGPT/Codex directory publication.
- Run commit, push, marketplace refresh, installation, or public submission only when the user requests those external effects.
- For a requested private marketplace release, validate, commit the narrow diff, push `main`, upgrade `mcook-plugins-local`, verify visibility, and reinstall only when requested. Start a new task before testing the installed skill.
- For public directory publication, follow current OpenAI submission documentation as a separate workflow. Do not assume that portable validation makes an archive acceptable to the OpenAI portal.
