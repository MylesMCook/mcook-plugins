# Accessibility

Taste that fails accessibility is not taste.

Use this file when recommendations risk becoming quiet, low-contrast, over-animated, or too dependent on visual nuance.

## Accessibility floor

### 1. Contrast
- Do not soften contrast just to look premium.
- Text, controls, chart labels, and key metadata must remain readable in realistic lighting conditions.
- If using muted palettes, concentrate contrast on the parts that carry task meaning.

### 2. Hierarchy without color dependence
- Never rely on color alone to distinguish status, priority, or selection.
- Use position, weight, labels, icons, pattern, shape, or grouping as well.

### 3. Typography
- Body text must be comfortable at the medium’s actual viewing distance.
- Tight tracking, thin weights, and low-contrast gray text often signal “taste” while actually killing readability.
- Small labels, captions, and chart notes still need deliberate size and contrast.

### 4. Interaction states
- Focus, hover, active, disabled, error, and success states must be visible and consistent.
- Keyboard focus should never disappear into a subtle glow or near-invisible outline.
- If a control looks quiet, its interaction state must do more work.

### 5. Motion
- Motion should clarify change, not merely decorate it.
- Keep timing restrained and predictable.
- Avoid parallax, blur reveals, or delayed fades that slow task completion or create discomfort.
- If motion is essential, allow it to be reduced.

### 6. Dense information
- Dashboards, tables, forms, and editorial pages need accessibility in structure, not only in surface styling.
- Preserve scannability with grouping, white space, headings, row states, and clear labels.
- Chart annotations, legends, and anomalies must be readable without guessing.

## Web implementation checks

For web work, test the relevant [WCAG 2.2 success criteria](https://www.w3.org/TR/WCAG22/) in the rendered interface:

- Text contrast: at least 4.5:1 for normal text and 3:1 for large text, subject to the criterion's exceptions ([1.4.3, AA](https://www.w3.org/TR/WCAG22/#contrast-minimum)).
- Essential visual boundaries and states of controls and graphics: at least 3:1 against adjacent colors where the criterion applies ([1.4.11, AA](https://www.w3.org/TR/WCAG22/#non-text-contrast)).
- Status, selection, and meaning have a cue besides color ([1.4.1, A](https://www.w3.org/TR/WCAG22/#use-of-color)).
- Keyboard users can reach controls, see focus, and keep the focused item at least partly visible ([2.1.1, A](https://www.w3.org/TR/WCAG22/#keyboard), [2.4.7, AA](https://www.w3.org/TR/WCAG22/#focus-visible), [2.4.11, AA](https://www.w3.org/TR/WCAG22/#focus-not-obscured-minimum)).
- Pointer targets meet the 24 by 24 CSS pixel minimum or an allowed spacing/other exception ([2.5.8, AA](https://www.w3.org/TR/WCAG22/#target-size-minimum)).
- Content reflows without loss of information or function at the specified narrow viewport/zoom conditions, except content that requires two-dimensional layout ([1.4.10, AA](https://www.w3.org/TR/WCAG22/#reflow)).

These are checks relevant to visual critique, not a complete WCAG audit or proof of conformance. Test the actual states and responsive layouts. For other media, apply the applicable accessibility standard and viewing conditions.

## Useful self-check

Before finalizing, ask:
- Did I make anything prettier but harder to read?
- Can the main task still be completed quickly?
- Are states visible without color alone?
- Would this still work on a bad laptop screen, in sunlight, or at arm’s length?
