# Skill ownership and mixed projects

Select by the component and requested change, using its imports, implementation, and styling contract. Repository-wide dependency presence is evidence, not a routing rule.

| Request | Lead | Supporting guidance |
| --- | --- | --- |
| Base UI dialog styled with StyleX | `base-ui-stylex` | `stylex` for general styling; testing for observed interaction |
| StyleX compiler or CSS extraction failure | `stylex` | Load this integration skill only if a Base UI boundary is implicated |
| Existing shadcn component edit or explicit shadcn request | `shadcn` | Preserve that component's existing conventions |
| Base UI + StyleX component in a project with `components.json` | `base-ui-stylex` | Read the actual component; do not import shadcn conventions |
| Plain React rendering or performance work | React performance skill when relevant | No Base UI workflow solely because the dependency exists |

Base UI supplies behavior and accessibility mechanics; StyleX supplies styling for new work using this stack. Native HTML remains appropriate where no additional behavior is needed. Existing project choices remain in place unless migration is explicitly requested.

`stylex` remains independently useful: it owns framework/compiler integration, extraction, authoring syntax, tokens, themes, typed style contracts, general migration, and styling debugging. This skill owns Base UI component selection, anatomy, callbacks, composition, portals, positioning, forms, and interaction verification. General StyleX themes belong there; carrying those themes across a Base UI portal belongs here.

Do not let Tailwind, `cn()`, shadcn variants, or Radix-style `asChild` conventions govern Base UI + StyleX components. Some shadcn components themselves use Base UI behavior: editing those existing source components still follows their actual shadcn styling contract. Base UI imports alone do not imply a StyleX migration.

Composition, TypeScript, performance, and testing skills support a concrete need. Do not load every frontend skill for every task. These are skill handoffs, not a requirement to spawn agents.

When `stylex` is unavailable, use the current [StyleX LLM resources](https://stylexjs.com/docs/llm-resources) for installation and authoring. Keep source links standalone; do not depend on relative paths into another installed skill.
