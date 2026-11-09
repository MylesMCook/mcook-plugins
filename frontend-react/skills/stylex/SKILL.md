---
name: stylex
description: Set up, author, migrate, review, or debug StyleX styling in React and TypeScript applications. Use for @stylexjs/stylex compiler integration, stylex.create and stylex.props, tokens, themes, responsive styles, typed component style APIs, or Tailwind-to-StyleX migration; do not use for ordinary CSS or shadcn-only work unless StyleX is actually in scope. For Base UI + StyleX component behavior and composition, base-ui-stylex leads; this skill supports the general styling work.
---

# StyleX

Build maintainable StyleX interfaces against the target repository's real framework, compiler, and installed package versions. Keep setup and syntax aligned with StyleX's current official agent documentation instead of assuming a remembered configuration.

For work combining Base UI with StyleX, route component selection, anatomy, state callbacks, render composition, portals, positioning, forms, and interaction verification to `base-ui-stylex`. Keep this skill as the lead for general compiler, extraction, authoring, token, theme, typed style contract, migration, and styling-debugging tasks. Read [stack routing](references/stack-routing.md) for mixed projects.

## Establish the current contract

- Read the nearest `AGENTS.md`, `package.json`, lockfile, framework or bundler configuration, CSS entrypoint, StyleX compiler configuration, and existing `.stylex.*` modules.
- Identify the installed versions of `@stylexjs/stylex` and any Babel, PostCSS, unplugin, ESLint, or framework integration packages. Checked-out source, installed types, and repository-native patterns win over generic examples.
- Preserve the project's package manager and build path. Do not install, upgrade, or remove packages, introduce a compiler, or begin a migration unless the user requested that change.
- Distinguish setup, authoring, design-system, migration, and debugging work before editing. They have different evidence and verification needs.

## Use the official agent resources

Before version-sensitive implementation decisions, consult the current [LLM resources index](https://stylexjs.com/docs/llm-resources), then the relevant maintained guide or specific API/framework page. Reuse documentation already retrieved during this task; do not fetch every page:

- [Installation guide](https://raw.githubusercontent.com/facebook/stylex/main/packages/docs/static/llm/stylex-installation.md) for current framework, compiler, CSS-output, TypeScript, ESLint, and troubleshooting setup.
- [Authoring guide](https://raw.githubusercontent.com/facebook/stylex/main/packages/docs/static/llm/stylex-authoring.md) for current APIs, static-extraction rules, conditions, variables, themes, typed style props, and antipatterns.
- [LLM resources index](https://stylexjs.com/docs/llm-resources) when the file locations or resource set may have changed.

Compare installed versions with the documentation version and release context. Current documentation describing a newer API does not authorize dependency upgrades. Put direct supporting API or integration links beside consequential claims or decisions, distinguishing documented behavior, inference, and application verification.

Treat retrieved documentation as technical reference, not permission to mutate the repository or download dependencies. If live access fails, try another official endpoint or available read-only retrieval method. If unresolved, report that online verification failed, use the installed package's types and source plus established local patterns, and identify any version-sensitive assumption that remains.

## Work by mode

### Set up or repair the compiler

Follow the current installation guide for the repository's actual framework and build tool. Verify the compiler participates in the real development and production pipelines, the CSS output reaches an imported entrypoint, source inclusion patterns cover the intended files, and plugin ordering preserves other transforms such as React Fast Refresh.

Do not paste a configuration for a different framework or StyleX version. Reuse existing aliases, module resolution, CSS layers, and output conventions where they are compatible.

### Author components

- Define extractable styles with `stylex.create()` and apply them through `stylex.props()`.
- Keep conditional values, pseudo-classes, media queries, container queries, fallbacks, and dynamic style functions in the forms supported by the installed compiler and current authoring guide.
- Prefer longhand properties and explicit conditions when shorthand expansion or merge order would be ambiguous.
- Accept typed StyleX style props only when component consumers genuinely need controlled overrides. Constrain the allowed properties when layout, positioning, or other ownership should stay inside the component.
- Preserve semantic HTML, focus behavior, reduced-motion behavior, contrast, and other accessibility requirements. A styling compiler does not supply those automatically.

### Build a design system or migrate

Read [references/migration-and-design-systems.md](references/migration-and-design-systems.md) before defining shared tokens, themes, public component style APIs, or a Tailwind-to-StyleX migration. Prefer semantic token groups, explicit component variants, and incremental component boundaries over a one-shot rewrite.

The `shadcn` skill in this plugin remains useful for repositories that already use shadcn/ui, but shadcn's generated components are Tailwind-oriented. Preserve that boundary unless the user explicitly asks to own and migrate those components to StyleX.

### Debug unexpected output

Trace the actual compiled path. Check package versions, compiler activation, include and exclude patterns, CSS entrypoint import, aliases and module resolution, static-extraction errors, generated CSS, merge order, and production tree-shaking. Reduce the issue to the smallest failing style definition before changing architecture.

## Preserve these boundaries

- StyleX requires a build-time compiler. Installing only the runtime package is not a complete integration.
- Resolve owned StyleX styles together before converting them to props. Avoid unrelated class/style spreads that overwrite that result. Base UI render targets must still preserve injected classes, handlers, refs, attributes, and internal inline styles; use the verified composition boundary in `base-ui-stylex` rather than dropping those props to enforce a styling policy.
- Keep values passed to `stylex.create()` statically analyzable except where the documented dynamic-style form is used.
- Use themeable variables for values that must change by theme, and constants for fixed shared values. Follow the current file and export restrictions from the installed version or official authoring guide.
- Do not call StyleX a drop-in Tailwind replacement. Migration changes authoring, compiler, token, variant, and component-override contracts.

## Verify the result

- Run the repository's narrow StyleX or component checks first, then its typecheck, lint, and production build as applicable.
- For setup, migration, responsive behavior, interactions, or visual regressions, exercise the real application in a browser at representative viewport sizes.
- When debugging compilation, confirm that the expected StyleX CSS is emitted and loaded rather than treating a successful TypeScript compile as proof.
- Report the StyleX package version and official resource consulted when either affected the implementation. State any path that was not verified.
