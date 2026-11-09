# Frontend / React

Build, refactor, style, type, optimize, and test React applications in Codex with eight pinned
third-party Agent Skills and two plugin-owned skills: Base UI + StyleX and StyleX.

## Included skills

- `base-ui-stylex` — Base UI component behavior and accessibility mechanics integrated with StyleX styling.
- `vercel-react-best-practices` — React and Next.js performance guidance from Vercel.
- `vercel-composition-patterns` — scalable React component API and composition patterns.
- `shadcn` — shadcn/ui project, component, registry, styling, and composition workflows.
- `webapp-testing` — live verification with Playwright CLI and repository-native browser regressions.
- `typescript-advanced-types` — advanced generics, conditional types, mapped types, and utilities.
- `stylex` — StyleX setup, authoring, tokens, themes, typed component APIs, migration, and debugging.
- `fixing-accessibility` — targeted repairs for names, keyboard access, focus, semantics, and forms.
- `fixing-motion-performance` — diagnose and repair animation jank within the existing stack.
- `fixing-metadata` — page titles, canonical URLs, social previews, and structured metadata.

The package has no MCP server, hooks, app, custom agent, background process, or runtime updater. It
uses the tools already available to Codex and the target repository. The testing skill uses the
installed official Playwright skill for live browser work and the project's existing test runner
for durable regressions. Other browser tools require an explicit request or a missing capability.

## Codex-native boundary

The upstream skills remain recognizable and traceable, but the package removes non-portable command
embedding and host-specific tool allowlists. The shadcn workflow inspects the real repository first, prefers an
installed project-local CLI, and asks before downloading a CLI or running a mutating command. The
testing workflow uses Playwright CLI for live observation and the repository's committed Playwright
setup for durable regressions. It does not install browsers or Python dependencies without
authorization. It also separates application verification from Codex annotation-mode verification
and provides a strict-CSP diagnostic for annotation-only failures. The authored StyleX skill is
Codex-native and reads StyleX's current
official LLM installation or authoring guide when version-sensitive details matter.

For new work using Base UI + StyleX, Base UI supplies component behavior and accessibility mechanics; StyleX supplies styling. Preserve existing project choices unless migration is explicitly requested.

`base-ui-stylex` leads component integration; `stylex` owns general compiler, extraction, authoring, tokens, themes, typed style contracts, migration, and styling debugging. `shadcn` applies to existing shadcn components or explicit requests. Route mixed projects by the component being changed, not the presence of `components.json`. The UI Skills additions apply to the named accessibility, motion, or metadata problem without changing the component's styling system. React performance, composition, TypeScript, and testing remain supporting guidance. See the [routing reference](skills/base-ui-stylex/references/skill-routing.md).

## Upstream updates

`upstreams.lock.json` pins the eight third-party skills to exact source commits. The repo-side
`scripts/sync_frontend_react.py` command refreshes the selected directories, reapplies the narrow
Codex compatibility transform, updates the lock, and bumps this plugin's patch version when an
upstream commit changes.

Maintain `base-ui-stylex` directly in `frontend-react/skills/base-ui-stylex` in this repository, just like `stylex`. The upstream sync never replaces either plugin-owned skill. The standalone copy in [mcook-skills](https://github.com/MylesMCook/mcook-skills/tree/main/skills/base-ui-stylex) is an optional export from this plugin, not an incoming source. Edit and release the plugin first; refresh the standalone copy only when needed. See [maintenance](skills/base-ui-stylex/references/maintenance.md).

Use `--locked` to reproduce recorded commits and `--upstream <name>` to limit a refresh. Unselected upstream pins and files stay unchanged. The shadcn compatibility transform preserves component-based routing on subsequent syncs.

The Base UI skill uses the entire live [Base UI index](https://base-ui.com/llms.txt) as its documentation map and fetches only relevant pages. Both skills require version checks, direct supporting citations, honest failed-verification reporting, and reuse of already retrieved docs. Newer docs do not authorize dependency upgrades.

The StyleX skill does not vendor a documentation snapshot. It routes version-sensitive work to
StyleX's live official [LLM resources](https://stylexjs.com/docs/llm-resources), so documentation
updates are available without waiting for a plugin release.

The scheduled `sync-frontend-react.yml` workflow runs weekly and opens or refreshes a pull request
when upstream content changes. It does not write directly to `main`, and installed Codex plugin
caches never modify themselves. The repository must allow GitHub Actions to create pull requests;
keep that one-time repository setting disabled until this workflow is published and approved.

After an update is merged and published to `mcook-plugins-local`, refresh this machine with:

```text
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add frontend-react@mcook-plugins-local
codex plugin list
```

Then start a new Codex task so the refreshed skill metadata loads cleanly.

## Validation

The [evaluation record](evals/validation.md) covers routing, package checks, and a compiled dialog. The reproducible [dialog fixture](https://github.com/MylesMCook/mcook-plugins/tree/main/scripts/evals/frontend-react-dialog) lives outside the plugin bundle.

## Sources and licenses

The Vercel, shadcn, wshobson, and UI Skills material is MIT-licensed. Anthropic's web application testing skill
is Apache-2.0-licensed. The Base UI + StyleX skill was originally imported from the MIT-licensed mcook-skills catalog and is now maintained here. The StyleX skill, packaging, and sync automation are original MIT-licensed
work informed by linked official documentation. The three UI Skills were discovered through the [UI Skills MCP](https://www.ui-skills.com/mcp) and pinned to their GitHub source. See
[ATTRIBUTION.md](ATTRIBUTION.md), [LICENSE](LICENSE), the bundled license files, and the license file
inside `skills/webapp-testing`.

## Framework coordination

For RedwoodSDK applications, use Redwood Web Apps for routing, server functions,
RSC behavior, and Cloudflare deployment, and Frontend / React for Base UI,
StyleX, and browser verification. Consult current framework docs when that
plugin is unavailable. Preserve existing Hono, Next.js, and other frameworks.
Next.js-specific performance examples do not apply automatically to Redwood.
Build Web Apps remains available for its distinct provider and image-led
workflows; choose one owner for overlapping frontend work in a given task.
