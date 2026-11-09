---
name: tufte
description: Tufte-led design standard for charts, dashboards and analytics pages. Use when building or changing any chart, graph, KPI tile, dashboard, report page, Power BI visual, or Vega-Lite/Deneb spec, and when asked to review, critique or audit one from a screenshot, code, PBIR export or live page. Loads a cited rulebook covering integrity, comparisons, encoding, color, words, type size and layout that default LLM output gets wrong.
---

# Tufte

Apply `references/rulebook.md` as the design standard. Two modes:

- **Build** (default): you are producing or changing a visual.
- **Review**: the user asks you to review, critique, audit or score one.

Read `references/rulebook.md` in full before either mode. Each rule names the
"LLM default" it corrects; those defaults are what you will drift toward.

## Build

1. Name the thinking task for yourself: who reads it, which decision or
   question it serves, how often, and the context (operational, analytical,
   strategic). Infer it from the request and data; state the assumption in
   one line if you had to guess. Do not print the audience or question on
   the page.
2. Build with the rules applied. The ones that change the most output:
   - Headline states the finding (G1), and every headline number has a
     comparison: prior period, target, or peer (B1). Never invent a target
     the user or data did not give.
   - Bars start at zero; no dual value axes; no gauges, 3D or many-slice
     pies (A2, A7, D2, D3).
   - Gray by default with one accent; direct labels instead of legends;
     never red versus green alone (F1, G2, F3).
   - Partial periods, gaps and data quality are visible (A6).
   - Word budgets (G7): headline 14 words or fewer, no intro paragraphs,
     insights blocks or methods sections.
   - Type minimums (G6) and nothing clipped or overlapping (C9). Fit by
     cutting content, never by shrinking type or panels.
   - One footer with source, refresh time, scope and owner (I1).
3. An existing design system or brand sets fonts and colors. It never
   overrides the integrity rules in section A.
4. Before handing off, check the result against the rulebook's Blockers and
   Majors and fix what fails. If you can render the page, check it at the
   target viewport for type size, clipping and horizontal scroll.
5. In your reply, name any rule you deliberately broke and why (see the
   contested rulings in section J). Do not list the rules you followed.

## Review

1. Follow the rulebook's **Review protocol** in order. Use every input you
   have: read source code or PBIR/Deneb JSON when present; render live pages
   when you can.
2. Report at most 7 findings, ranked: every Blocker, then Majors by how much
   they block the task, then Minors. For each give:
   - rule ID and severity
   - where on the page
   - the evidence you saw
   - the fix, with a Power BI path when relevant
   - the source as the rulebook cites it
3. Say when a finding is inferred from a screenshot alone. Cite only sources
   that appear in the rulebook. Present `[P]` rules as judgment, not
   literature.
4. End with a **Keep** list of up to 2 things a redesign must preserve.
5. Do not edit files in Review mode unless the user asks for fixes.

## Do not

- Invent data, targets, sources, owners or refresh times. Mark a missing
  footer fact as missing.
- Quote book text. The rulebook paraphrases and cites.
