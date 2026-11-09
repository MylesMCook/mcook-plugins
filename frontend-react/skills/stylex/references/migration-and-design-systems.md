# StyleX design systems and migrations

Read this reference when work affects shared tokens, themes, public component style APIs, or an existing styling system. It supplements StyleX's current official installation and authoring guides; it does not replace them.

## Design-system shape

1. Inventory the current styling sources: global CSS, resets, fonts, CSS modules, utility classes, inline styles, third-party components, and generated shadcn/ui components.
2. Group shared values by meaning rather than by raw value. Use semantic names for color, typography, spacing, radius, elevation, motion, and layout decisions that consumers should share.
3. Use `stylex.defineVars()` for values that must be themed or overridden at runtime. Use `stylex.defineConsts()` for fixed shared values such as stable breakpoints or animation names. Confirm the current file and export restrictions in the official authoring guide.
4. Build component styles from a base plus explicit variants, sizes, states, and controlled consumer overrides. Avoid recreating an unrestricted utility string API around StyleX.
5. Keep global CSS for genuinely global concerns such as resets, fonts, document defaults, and third-party integration seams. Do not force every stylesheet through StyleX merely to claim purity.

## Incremental migration

Migrate at component boundaries:

1. Capture the component's visual, responsive, interactive, and accessibility behavior before changing it.
2. Move leaf components first, then shared primitives once their consumer contracts are understood.
3. Keep the old and new styling systems on separate elements or components during coexistence. Avoid overwriting unrelated `className` or inline `style` values with `stylex.props()` on one element. At a Base UI render boundary, preserve and merge injected behavior props and internal styles using `base-ui-stylex`; these are required integration props, not an alternate public styling API.
4. Translate design tokens and variants deliberately. Do not mechanically convert utility strings one token at a time when the result should be a semantic component style.
5. Run type, build, browser, and visual checks for each migrated slice.
6. Remove old dependencies, compiler configuration, CSS directives, and helper utilities only after repository-wide usage checks show they are no longer needed.

Prefer a reversible series of component migrations over a repository-wide flag day. Do not hide a mixed-system state behind a generic abstraction that makes ownership or precedence unclear.

## shadcn/ui boundary

shadcn/ui distributes source components whose normal styling contract is Tailwind-oriented. In an existing shadcn project:

- Keep generated or already-owned shadcn components on their current styling path unless migration is explicitly requested.
- Treat a Tailwind-free shadcn migration as component ownership work: replace the class-based styles, variants, merge helpers, and tokens component by component.
- Expect a later shadcn CLI update to reintroduce upstream Tailwind-oriented code. Decide whether the project will stop consuming generated updates, maintain a transformation, or repeat a reviewed migration.
- Do not remove Tailwind until both application code and owned shadcn components are free of required classes, directives, plugins, and token definitions.

## Review checklist

- Themeable and fixed tokens use the appropriate StyleX primitive.
- Component variants are explicit and type-safe.
- Consumer style props expose only properties the component can safely surrender.
- Responsive, pseudo-state, reduced-motion, and theme behavior match the original contract.
- Styling-system precedence is obvious at every coexistence boundary.
- Production output includes the expected StyleX CSS without retaining dead legacy CSS.
