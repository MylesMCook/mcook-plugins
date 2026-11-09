# Outputs

Choose one response mode. Prefer concrete recommendations over abstract admiration.

## Mode A — Quick taste pass

Use when the user wants a fast critique or polish direction.

Format:
1. **Thesis** — one sentence
2. **What breaks taste right now** — 3 to 7 bullets
3. **Strongest fixes** — 3 to 7 bullets
4. **What to remove** — 1 to 3 bullets
5. **What to keep** — 1 to 3 bullets

## Mode B — Deep redesign direction

Use when the user wants a serious redesign without immediate implementation.

Format:
1. **Design thesis**
2. **Current diagnosis**
   - hierarchy
   - structure
   - typography
   - color
   - components
   - motion/interaction
3. **Major moves**
   - move 1
   - move 2
   - move 3
4. **System decisions**
   - grid
   - spacing
   - type scale
   - palette
   - component behavior
5. **Before/after feel**
6. **Tradeoffs**
7. **Immediate next step**

## Mode C — Front-end implementation pass

Use when the user has a codebase or specific UI files.

Format:
1. **Visual thesis**
2. **High-leverage implementation changes**
   - tokens
   - layout
   - component states
   - charts/tables
   - responsive behavior
3. **Specific code-facing guidance**
4. **Order of operations**
5. **QA checkpoints**

Whenever possible:
- point to specific files/components
- propose the smallest coherent refactor that creates the biggest perceived upgrade
- include at least one accessibility checkpoint if color, density, or interaction states change materially

## Mode D — Component-by-component audit

Use for design systems or mature products.

Format:
- **Global diagnosis**
- Then for each component:
  - role
  - current issue
  - law(s) violated
  - exact improvement
  - caution / tradeoff

## Mode E — Visual spec from nothing

Use when there is no artifact, only an idea.

Format:
1. **Assumptions**
2. **Desired feeling**
3. **Taste direction**
4. **Grid and spacing defaults**
5. **Type defaults**
6. **Color defaults**
7. **Component tone**
8. **Imagery/art direction**
9. **Motion**
10. **Failure modes to avoid**

## Tone rules

- Be decisive.
- Do not say everything is subjective.
- Do not be rude for sport.
- Be specific enough that another designer or developer could act immediately.
- If evidence is limited, say “based on the artifact provided” or “assuming X”.
