# Frontend / React evaluation

## 0.3.1 Playwright CLI routing correction

Evaluated 2026-09-22 in the isolated release checkout. The `webapp-testing` entrypoint now uses the installed Playwright CLI skill for live exploration and the target repository's test runner for durable regression coverage. The sync transform retains this routing after an upstream refresh. Bundled upstream Python files remain available for existing consumers, but the entrypoint no longer selects them by default.

- Ten sync and framework-overlay tests pass under Python 3.13, including a regeneration check for Playwright CLI routing.
- The portable package and OpenAI overlay validator passes with zero warnings; `webapp-testing` frontmatter validates.
- JSON parsing and `git diff --check` pass. No live browser flow was run for this guidance change.

## 0.3.0 UI Skills addition

Evaluated 2026-09-22. UI Skills MCP `list_skills` and `get_skill` identified the three focused skills added in this release. The source is pinned to `fd0889bdf72aee45c32028b4643b09735d5b5a34`. `baseline-ui` was reviewed and excluded because its mandatory Tailwind and `cn()` rules conflict with the plugin's StyleX workflow.

- Agent Plugins package and OpenAI overlay validation pass with zero warnings.
- All three added skills pass frontmatter validation. The unsupported upstream `version` key in `fixing-metadata` is removed by a tested sync transform.
- Seven sync tests pass under Python 3.13, including selective refresh, dirty-file protection, and the new metadata transform.
- `git diff --check` passes. The routing cases below are reviewed against the skill descriptions and bodies; no live application acceptance was run for these advisory skills.

## 0.2.1 ownership change

Evaluated 2026-09-08. Base UI + StyleX is now authored directly in the plugin, alongside StyleX. The mcook-skills copy is an optional outward export; its former incoming pin has been removed. The source pin below describes the historical 0.2.0 import only.

- All 94 repository tests pass, including a regression that preserves both committed and uncommitted plugin-owned edits through sync.
- A full remote `--locked` replay preserves every plugin byte while the plugin-owned skill has local edits.
- Portable and OpenAI plugin checks and the changed skill's frontmatter validation pass.
- Standalone catalog discovery, frontmatter lint, and universal installation pass; the existing pi-package-creator license-key warning remains unrelated.
- Component integration guidance and application fixture code are unchanged; the 0.2.0 dialog verification below remains the behavioral evidence.

## 0.2.0 historical evaluation

Evaluated 2026-09-08. The canonical Base UI + StyleX skill is pinned to `dc89eec1478cf84f55eb61fd7349ec25ca7ef2d5` in mcook-skills. The other four repository pins are unchanged. The bundled skill, including metadata and references, matches the canonical source byte-for-byte.

## Routing review

Reviewed the actual frontmatter, skill bodies, and references against all twelve requests in [routing.json](routing.json). This is a manual routing evaluation, not a statistical model-selection benchmark.

| Request | Result |
| --- | --- |
| Base UI dialog with StyleX | `base-ui-stylex` leads; general StyleX and testing support it |
| Compiler or missing extracted CSS | `stylex` leads |
| Existing shadcn edit | `shadcn` leads; existing styles stay in place |
| Base UI + StyleX inside a components.json project | `base-ui-stylex` leads from the component's actual stack |
| Plain React performance | React performance guidance; no Base UI workflow |
| shadcn component using Base UI internally | `shadcn` leads from the existing styling contract |
| Ambiguous dialog in a mixed project | Inspect the component before selecting the workflow |
| Online documentation unavailable | Try official fallback; report unresolved verification and local evidence |
| New docs exceed installed version | Use compatible local behavior; no incidental upgrade |
| Unlabeled controls and broken focus | `fixing-accessibility` leads; preserve the component stack |
| Janky drawer transition | `fixing-motion-performance` leads; keep the existing animation library |
| Wrong social preview and duplicate canonical | `fixing-metadata` leads |

## Observed checks

- mcook-skills catalog discovery: 36 skills; target universal installation and installed frontmatter verification pass.
- mcook-skills GitHub `validate-skills` CI passes at the pinned commit, including its catalog-wide smoke-install matrix.
- Full `sync_frontend_react.py --locked` replay from remote Git commits produces no changes to the plugin files, pins, or version.
- Catalog frontmatter lint: zero errors; one pre-existing `license`-key warning in pi-package-creator.
- Portable package: passes with zero warnings; OpenAI overlay and all seven Frontend / React skills validate.
- Repository tests: 85 pass, including five tests for sync reproduction, selective updates, pin/version behavior, dirty-file protection, and changed-anchor failure.
- All 22 locally cataloged portable packages validate. Unrelated unpublished catalog edits were preserved.
- Dialog fixture: StyleX ESLint rules, strict TypeScript, and production build pass. Expected extracted CSS is emitted and verified through computed styles.
- Real Chrome: both 1280x720 and 375x667 cases pass. Keyboard opening, focus entry/containment/return, focus visibility, accessible name/description, modal isolation, Escape/Close/backdrop dismissal, consumer handler preservation, static/dynamic state styles, live portal theme changes, and viewport containment were observed. No browser console or page errors remain.

The dialog follows the current [Base UI part APIs](https://base-ui.com/react/components/dialog), [composition](https://base-ui.com/react/handbook/composition), and [mergeProps contract](https://base-ui.com/react/utils/merge-props). The compiler follows [StyleX's Vite guide](https://stylexjs.com/docs/learn/installation/vite/vite-react). Portal theme application is an integration decision based on [DOM theme inheritance](https://stylexjs.com/docs/learn/theming/creating-themes/) and verified by browser colors.

Base UI 1.8.0 matches the current component documentation and release page. StyleX runtime/compiler/linter are 0.19.0; React is 19.2.8. The fixture's exact toolchain is recorded in its lockfile. It uses the existing Chrome installation, not a downloaded Playwright browser. The initial reader rejected Base UI Markdown MIME types; direct official HTML and curl retrieval succeeded, so online verification was completed.

## Limits

This evaluates one dialog in Chrome at two viewport sizes. It does not establish screen-reader speech, other browser engines, SSR/hydration, forms, anchored positioning, animated lifecycle behavior, or every Base UI component. No existing application or dependencies were migrated. Fresh installed discovery and local cleanup are release checks reported in the task handoff.
