# Myles Plugin Builder

Build portable Agent Plugins and OpenAI-compatible plugins for this marketplace.

## Included skill

- `build-mcook-plugin` selects the portable, OpenAI-native, or dual package contract; keeps MCP packaging separate from MCP wire-protocol compatibility; registers the package in `.agents/plugins/marketplace.json`; and runs target-specific validation.

The skill uses the local repository layout: plugin folders live at the repository root and marketplace entries use relative paths such as `./plugin-name`.

## Use in Codex

```text
$mcook-plugin-builder:build-mcook-plugin Create a marketplace-ready Codex plugin for this workflow.
```

Portable packages follow [Agent Plugins 1.0.0](https://agent-plugins.org/specification), including root `plugin.json`, fixed component discovery, root `mcp.json`, and canonical schemas. The builder includes an `uv`-native validator for schema, path, transport, secret, overlay, and marketplace checks.

OpenAI-native and compatibility layers continue to follow OpenAI's current [plugin packaging documentation](https://developers.openai.com/plugins/build/plugins). They remain a separate contract from the portable core.

Every release must pass the skill's [Agent Plugins conformance gate](skills/build-mcook-plugin/SKILL.md#release-deliberately) or carry an explicit, evidence-backed native-only exception in its README. Native-only packages must state their compatibility limits and pass the applicable native checks; they cannot claim Agent Plugins conformance.

The portable validator accepts both repository package roots and Codex's
versioned installed-cache layout, so the same package checks can prove source
and installed bytes without renaming the cache.

MCP `2026-07-28` is also separate. The skill documents Codex's opt-in mode and requires modern discovery, stateless metadata, pagination, cache fields, multi-round input, and transport-specific tests before claiming support. See the MCP [key changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog).

It targets the private `mcook-plugins-local` marketplace. Public publication to the shared ChatGPT/Codex Plugins Directory remains a separate submission and review workflow.

## License

MIT. See [LICENSE](LICENSE).

## Marketplace source validation

The Codex catalog contains `cici@mcook-plugins-local`, the repository-owned replacement for Claude Code Advisor. See [Cici](../cici/README.md) for the three direct CLI skills and migration order.

External metadata uses the documented Codex `git-subdir` (or repository-root `url`) contract, credential-free GitHub HTTPS and exactly one full commit `ref` or `sha`. Local entries remain inside the marketplace root. The builder’s metadata-only mode does not establish package validity, remote availability, license compatibility, or installed-byte identity:

```sh
uv run mcook-plugin-builder/skills/build-mcook-plugin/scripts/validate_agent_plugin.py --marketplace-entry cici --marketplace .agents/plugins/marketplace.json --marketplace-root .
```

Separately inspect the pinned package and validate an isolated installation. Keep external native packages in their original format; the portable validator is not an OpenAI-native validator. See [Codex marketplace source documentation](https://developers.openai.com/plugins/build/plugins#marketplace-metadata).
