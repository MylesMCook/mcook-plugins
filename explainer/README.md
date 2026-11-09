# Explainer

Ask how something works and get an interactive explainer: one HTML page that draws the parts as small isometric icons, plays the messages between them step by step, and lets you open each message to read what was sent.

Install in Claude Code:

    /plugin install explainer --marketplace MylesMCook/mcook-plugins

In Codex: `codex plugin add explainer@mcook-plugins-local`, then start a new task.

Try:

- "Explain how OAuth sign-in works, as an explainer."
- "Turn this incident write-up into an explainer I can step through."
- "Make an explainer of how our deploy pipeline works from these files."

Pages land in `~/Explainers/<id>.html` with the topic beside them as `<id>.json`. Ask an agent to revise the `.json` and rebuild to change a page. Set `EXPLAINER_OUT` to save somewhere else.

## What's inside

- **Skill `explainer`**: how to plan, write, check and build a topic, including accuracy and plain-writing rules.
- **MCP server `explainer`** (Node 18+, no dependencies, stdio): `explainer_guide`, `explainer_list`, `explainer_get`, `explainer_check`, `explainer_build` and `explainer_open`. Rebuilding a page keeps the previous version in `~/Explainers/.history/`. Build and open return a local link from one shared viewer that starts by itself and stops after 30 idle minutes or with the session.

The checker keeps every page on the same template: 11 icons, 6 message kinds, 3 zone styles, the fields in `topic.schema.json`, and length and wording limits. Presets (`protocol`, `incident`, `process`) fix the terms each kind of explainer uses.

## MCP protocol

The server answers both the `initialize` handshake (2024-11-05 to 2025-11-25) and MCP `2026-07-28` (`server/discover`, per-request `_meta`). Only the `initialize` handshake has been verified end to end in a real client (Claude Code). The package declares no `2026-07-28` opt-in.

## Source

Generated from [explainer-kit](https://github.com/MylesMCook/explainer-kit) with `node scripts/export-plugin.mjs <this plugin>/skills/explainer`. Edit the kit, not this copy. The kit holds the template screenshot tests.

## License

Code: MIT. Bundled fonts Geist, Geist Mono and Fragment Mono: SIL Open Font License 1.1 (`skills/explainer/src/fonts/`).
