# Attribution

`frontend-react` vendors eight selected third-party Agent Skills and keeps their original skill names,
supporting files, and license notices. Exact revisions are recorded in `upstreams.lock.json`. The
Base UI + StyleX and StyleX skills are maintained directly in this plugin.

## Base UI + StyleX origin

- Original source: <https://github.com/MylesMCook/mcook-skills>
- Original import: `dc89eec1478cf84f55eb61fd7349ec25ca7ef2d5` (historical provenance, not an active upstream pin).
- Skill: `skills/base-ui-stylex`
- License: MIT; preserved in `licenses/mcook-skills-MIT.txt`.
- Current source of truth: `frontend-react/skills/base-ui-stylex` in this repository. The standalone mcook-skills copy is exported from here when needed. All subsequent skill and metadata edits belong here.
- Documentation is linked live, not copied from Base UI or StyleX.

## Vercel Agent Skills

- Source: <https://github.com/vercel-labs/agent-skills>
- Skills: `skills/react-best-practices` and `skills/composition-patterns`
- Discovery: <https://www.skills.sh/vercel-labs/agent-skills/vercel-react-best-practices> and
  <https://www.skills.sh/vercel-labs/agent-skills/vercel-composition-patterns>
- License: MIT, as declared by the upstream repository and both skill manifests.
  The pinned repository has no standalone license or copyright notice file;
  the exact declarations and source links are recorded in
  [the Vercel source notice](licenses/vercel-agent-skills-NOTICE.md).
- Local changes: generated Codex `agents/openai.yaml` metadata only.

## shadcn/ui

- Source: <https://github.com/shadcn-ui/ui>
- Skill: `skills/shadcn`
- Discovery: <https://www.skills.sh/shadcn-ui/ui/shadcn>
- License: MIT; the upstream license is preserved in `licenses/shadcn-ui-MIT.txt`.
- Local changes: removed host-specific frontmatter and inline command expansion, removed an
  unsupported MCP client row, added a local-first Codex command boundary and component-based mixed-project routing, and normalized
  `agents/openai.yml` to Codex's `agents/openai.yaml` filename with a default prompt.

## Anthropic Skills

- Source: <https://github.com/anthropics/skills>
- Skill: `skills/webapp-testing`
- Discovery: <https://www.skills.sh/anthropics/skills/webapp-testing>
- License: Apache-2.0; the upstream `LICENSE.txt` remains inside the skill.
- Local changes: replaced the upstream Python-first instructions with a Playwright CLI workflow for
  live browser work and repository-native tests for durable regressions. The bundled Python server
  helper remains for existing consumers; stale Python examples are omitted. The overlay requires
  authorization before browser-tool installation and diagnoses strict-CSP failures in Codex annotation
  mode without weakening application policy.

## wshobson/agents

- Source: <https://github.com/wshobson/agents>
- Skill: `typescript-advanced-types`
- Discovery: <https://www.skills.sh/wshobson/agents/typescript-advanced-types>
- License: MIT; the upstream license is preserved in `licenses/wshobson-agents-MIT.txt`.
- Local changes: generated Codex `agents/openai.yaml` metadata only.

## UI Skills

- Discovery: UI Skills MCP at <https://www.ui-skills.com/mcp>, using `list_skills` and `get_skill`.
- Source: <https://github.com/ibelick/ui-skills> at the commit in `upstreams.lock.json`.
- Skills: `fixing-accessibility`, `fixing-motion-performance`, and `fixing-metadata`.
- License: MIT; preserved in `licenses/ui-skills-MIT.txt`.
- Local changes: generated Codex `agents/openai.yaml` metadata; removed the unsupported `version` frontmatter key from `fixing-metadata`.
- Selection: these focused skills work with existing React, Base UI, StyleX, or shadcn components. The catalog's `baseline-ui` was excluded because its mandatory Tailwind and `cn()` rules conflict with this plugin's StyleX path.

## StyleX

- Documentation: <https://stylexjs.com/docs/llm-resources>
- Source: <https://github.com/facebook/stylex/tree/main/packages/docs/static/llm>
- Local skill: `stylex`
- Local changes: original Codex-native workflow and migration guidance that links to StyleX's live
  official installation and authoring resources. No StyleX source code or documentation snapshot is
  vendored in this plugin.

The compatibility changes are deterministic and reapplied by `scripts/sync_frontend_react.py` after
each upstream refresh. If an expected upstream anchor changes, the sync fails instead of silently
dropping the Codex boundary.

The React best-practices skill and compiled AGENTS.md receive a local framework
ownership preamble. `adapt_react_framework` in the sync script reapplies it after
upstream refresh; it scopes Next.js APIs and coordinates RedwoodSDK work without
altering the pinned upstream rule bodies.
