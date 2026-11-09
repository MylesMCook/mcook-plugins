## Learned User Preferences

- For marketplace migrations, keep the legacy source intact until every required replacement installs and validates from the Git-backed marketplace; preserve stable internal IDs and remove duplicate catalog ownership only after migration succeeds.
- For completed plugins intended for the connected marketplace, publish the narrowly scoped plugin and catalog entry to the online repo, verify marketplace visibility, and leave installation to the user unless they explicitly ask for it.

## Learned Workspace Facts

- `AGENTS.md` is this repo's sole durable guidance and memory surface; do not add a second repo-memory system.
- `task-naming` is explicitly invoked only: it has no hooks, MCP server, background state, or automatic maintenance; `$task-naming` scopes to the current task, one project folder, or one machine, uses native task operations, and formats titles as action-first `Verb object` with an optional `— Context` suffix.
- `mcook-plugins-local` is this repo's canonical Git-backed marketplace ID; its display name is `Myles Codex Plugins`.
- `.claude-plugin/marketplace.json` serves Claude Code and claude.ai (ID `mcook-plugins`). Every listed package must have `.claude-plugin/plugin.json`; versions match the portable and Codex manifests. Keep component definitions in that manifest and use default `skills/` discovery. Exclude Fabric's executable package and packages with Codex-only hooks (such as `goalie`). Validate the catalog and every listed package with `claude plugin validate`; run `uv run --with pyyaml==6.0.3 python -m unittest discover -s scripts/tests` for cloud packaging checks.
- The canonical catalog is `.agents/plugins/marketplace.json`; local entries use contained relative `./` source paths. Reviewed external packages may use credential-free HTTPS `git-subdir`/`url` sources pinned to a full commit SHA.
- Locally authored portable catalog plugins live at the repository root and follow the Myles Plugin Builder portable-plus-OpenAI shape: root `plugin.json` plus `.codex-plugin/plugin.json`. Never edit or copy plugin source from `~/.codex/.tmp`; Codex may use that path only as its managed Git-marketplace checkout.
- For a new or materially revised Codex plugin in this repository, invoke `$mcook-plugin-builder:build-mcook-plugin` before changing files. It owns the plugin-versus-skill boundary, skills-first package, marketplace wiring, provenance, validation, and release boundary; keep this file to routing and durable repo facts.
- To refresh published plugins on a machine, close active tasks using them, run `codex plugin marketplace upgrade mcook-plugins-local`, verify with `codex plugin list`, and start a new task. Since Codex CLI 0.164.0 (observed 2026-10-26) the upgrade also refreshes every installed plugin from that marketplace; `codex plugin add <plugin-name>@mcook-plugins-local` is needed only for a first install. For Claude Code, run `claude plugin marketplace update mcook-plugins`, then `claude plugin update <plugin-name>@mcook-plugins` per installed plugin.
- Claude Code decides updates from the `version` in `.claude-plugin/marketplace.json`, not the package's `plugin.json`. Bump the catalog `version` (and keep `description` in sync) in the same change as every package release, or Claude reports the old version as latest.
- `thermos` is published in `mcook-plugins-local`; install it with `codex plugin add thermos@mcook-plugins-local`, then start a new task so its four skills load cleanly.
- The `continual-learning` plugin was retired because its blocking Stop-hook continuation polluted task history and made interactive reliability worse. Do not reintroduce automatic transcript mining, blocking Stop hooks, or private Codex-state reads; use standalone read-only Scheduled reports that propose evidence-backed `AGENTS.md` candidates for manual review and never apply changes.
- Marketplace consolidation is gated on fresh-home installation and validation of Deneb, Chrome DevTools, Canvas Apps, and MCP Server Dev; Chrome DevTools also has a real MCP handshake check.
- The repo-wide plugin validator currently fails on Caveman because its `agents/openai.yaml` icon paths escape the skill archive; treat that as a known pre-existing compliance defect, not a failure of the four-plugin migration gate.

- `frontend-react/skills/base-ui-stylex` and `frontend-react/skills/stylex` are authored in this repository. The mcook-skills `base-ui-stylex` copy is an optional outward export; never sync it back into the plugin. See the skill's `references/maintenance.md` for authoring and export guidance.

- Pstack and the standalone Adversarial Review package are retired from both catalogs. Thermos owns paired and adversarial review; Writer has one `writer` entrypoint. Retained retired source is for rollback, not new installation.

- `linear-project-manager` has a portable Agent Plugins core plus OpenAI compatibility, with no automatic hooks. It remains in the Codex catalog only. Keep both portable-only and compatibility fresh-home discovery checks, and the Linear MCP endpoint/transport parity check, passing before changing its package format.


- `cici` replaces the retired Claude Code Advisor and Claude Code packages with the three direct CLI skills. Keep its existing helper and skills stable; do not restore Advisor orchestration or add it to the Claude catalog.
