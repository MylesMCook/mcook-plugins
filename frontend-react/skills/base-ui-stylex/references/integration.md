# Integration boundaries

Use these rules after checking relevant live pages. Discover current component and utility links at https://base-ui.com/llms.txt.

## Static and state styling

For static styling, pass the complete `stylex.props(styles.part)` result to the Base UI part.

For state-dependent static styles, a documented `className(state)` callback may return `stylex.props(styles.base, state.checked && styles.checked).className`. Use this shortcut only when no composed style needs returned inline `style` values. Dynamic styles can require both fields.

For state-dependent dynamic styles, use the part's supported render callback and preserve its received props while applying the full StyleX result. Consult [styling](https://base-ui.com/react/handbook/styling) and the component docs for state fields. Do not assume checked, pressed, highlighted, or transition fields exist on every part.

Use supported pseudo-classes for focus-visible and hover. Do not paste Tailwind data variants or arbitrary CSS selectors into StyleX. Verify selector support in the installed compiler rather than claiming attribute selectors are universally supported or forbidden.

## Render composition

Base UI uses [render composition](https://base-ui.com/react/handbook/composition), not Radix's asChild API. Prefer element-form render when sufficient. Custom targets must forward refs and received DOM props using the project's React-version convention.

In callbacks, preserve handlers, ref, ARIA/data attributes, children, and internal inline styles. Avoid nested interactive elements.

[mergeProps](https://base-ui.com/react/utils/merge-props) merges handlers, classes, and inline styles, but does not merge refs. Use an existing supported ref-composition utility when another ref is needed.

A schematic Toggle callback boundary:

```tsx
render={(baseProps, state) => {
  const visualProps = stylex.props(
    styles.base,
    state.pressed && styles.pressed,
  );
  return <button {...mergeProps<'button'>(visualProps, baseProps)} />;
}}
```

This assumes StyleX and Base UI mergeProps imports, defined styles, and a Toggle API exposing pressed. Adapt and typecheck it; it is not a complete component. Preserve children supplied through baseProps. This ordering keeps Base UI's inline properties on conflicts. Separate authored visuals from library-owned positioning and measurement styles.

mergeProps concatenates classes; it does **not** perform StyleX conflict resolution. Resolve all owned StyleX objects together before converting to classes. Class-string order does not determine CSS precedence.

## Public wrappers and internal adapters

Derive app-facing wrapper behavior props from installed Base UI types. Use finite variants and, when needed, narrow typed StyleX part overrides. Avoid unrestricted className or inline-style public APIs where the wrapper owns appearance.

A low-level custom render target must still accept and forward injected className, style, handlers, and ref. Rejecting those to enforce a styling policy breaks composition. Keep this adapter boundary distinct from the public component API. Never pass a StyleX object to DOM style or resolve conflicts with broad any casts.

## Themes and overlays

[StyleX themes](https://stylexjs.com/docs/learn/theming/creating-themes/) use DOM inheritance. React context crossing a portal does not carry CSS variables from the wrapper the portal left.

Use a shared themed DOM ancestor, a suitable themed portal container, or a theme applied at the overlay boundary. Account for SSR/hydration before changing document-root ownership. Verify open popups change with the page theme.

Keep documented Portal/Positioner/Popup anatomy. Let Base UI own placement and collision handling; avoid overriding positioner transforms. Read the specific part's documented CSS variables for available space and anchor dimensions.

Consult the [quick start](https://base-ui.com/react/overview/quick-start) for isolation/stacking and [animation guide](https://base-ui.com/react/handbook/animation) for lifecycle behavior. Preserve mount/unmount semantics and reduced motion. Ordinary hover/focus state does not describe the entire enter/exit lifecycle.
