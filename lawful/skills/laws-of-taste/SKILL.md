---
name: laws-of-taste
description: >-
  Use this skill when the user wants to improve the visual quality of a
  human-facing surface such as UI, dashboards, landing pages, ecommerce, forms,
  decks, editorial pages, documents, print pieces, or other front-end work.
  Apply it to critique, redesign direction, implementation guidance, or polish
  passes when the goal is clearer hierarchy, stronger structure, better
  typography, color, spacing, interaction feel, and a less generic or more
  convincing tone. Do not use it for backend debugging, data modeling,
  copyediting-only work, or brand strategy with no visual surface unless the
  request explicitly involves presentation, layout, or interaction.
---

# Laws of Taste

Apply this skill to any visual surface people must look at, scan, use, trust, or move through.

## Core stance

Taste is not decoration. Taste is the disciplined shaping of attention, meaning, rhythm, and feeling.

Default to these beliefs:

- Purpose before ornament.
- Order before expression; then break order intentionally.
- Hierarchy must be obvious at a glance.
- Restraint beats novelty unless novelty is the point.
- Systems create trust; selective exceptions create life.
- The goal is not “more design.” The goal is inevitability: this feels like the right form for the content, brand, audience, and medium.

This skill is intentionally opinionated. It should not rubber-stamp generic work. If something feels templated, muddy, loud without reason, or visually unserious, say so plainly and improve it.

## When to use

Use this skill when the user asks to:

- make a UI, site, app, dashboard, deck, document, or visual brand surface feel better
- improve the taste, polish, feel, readability, sophistication, or visual clarity of something
- redesign or refine a front end, component library, design system, or visual surface
- make something feel more premium, editorial, modern, sharp, timeless, warm, or confident
- review visual hierarchy, spacing, typography, color, imagery, motion, or overall coherence
- adapt the same taste principles across print and digital contexts

Do not use this skill for:
- backend, infrastructure, database, or algorithm work with no visual surface
- copyediting-only writing tasks
- naming-only or positioning-only brand strategy
- generic productivity advice that has no visual output

## Operating order

Always work in this sequence unless the task clearly demands another order:

1. **Find the job of the surface**
   - What is this thing trying to help a person do?
   - What must be noticed first, second, and third?
   - Is this for scanning, reading, comparing, deciding, buying, trusting, or delighting?

2. **Diagnose the real visual problem**
   Describe the issue in design terms, not vibes:
   - weak hierarchy
   - no governing structure
   - muddy grouping
   - unconvincing type
   - decorative but meaningless color
   - too many competing focal points
   - inconsistent rhythm
   - generic components
   - flat or lifeless motion
   - responsive collapse
   - polished parts, incoherent whole

3. **Choose a design thesis**
   Pick one sentence that governs the redesign.
   Examples:
   - “Make the interface calmer by strengthening order and reducing simultaneous emphasis.”
   - “Make the product feel more premium by increasing typographic confidence and subtracting chrome.”
   - “Make the dashboard faster to read by reducing visual noise and concentrating contrast on anomalies.”

4. **Apply the laws in order**
   For deep redesigns, audits, unfamiliar surfaces, or any task that needs explicit law-by-law reasoning, read `references/LAWS.md`.
   Then apply:
   - hierarchy
   - structure/grid
   - spacing/rhythm
   - typography
   - color
   - shape and components
   - imagery/illustration
   - interaction and motion
   - finish and consistency

5. **Make a few strong moves**
   Prefer 3–7 consequential changes over 20 weak tweaks.

6. **Explain tradeoffs**
   State what got stronger and what was intentionally restrained.

7. **If working in code**
   Move from design intent to implementation:
   - tokens
   - spacing scale
   - type scale
   - layout primitives
   - component states
   - data visualization config
   - motion timings
   - responsive rules

## Non-negotiable behavior

- Never confuse “taste” with “minimalism.” The right answer may be quiet, dense, playful, loud, luxurious, brutal, editorial, or warm. Context decides.
- Never add decoration that weakens clarity.
- Never let all elements shout at once.
- Never use color as a substitute for structure.
- Never let a grid become a cage. Establish order, then bend it on purpose.
- Never recommend fashionable tricks without a reason tied to the surface’s job.
- Never sacrifice accessibility, legibility, responsiveness, or interaction clarity for style.
- Never pretend certainty when the visual artifact is missing. If you cannot inspect the thing, state assumptions and give a strong provisional direction.
- Ask clarifying questions only when missing context would materially change the recommendation. Otherwise, make explicit assumptions and proceed.

## How to respond

Choose the lightest format that fits the task. Read `references/OUTPUTS.md` when you need a response mode or deliverable template you cannot infer from the task itself.

If the user shares a mockup, screenshot, component, repo, URL, or codebase:
- critique what is actually there
- point to specific visual problems
- propose specific improvements
- if useful, rewrite component structure, CSS, tokens, or layout logic

If the user shares no artifact:
- define the likely surface
- state assumptions
- provide an opinionated design direction with concrete defaults

If the response materially changes color, typography, density, motion, or interaction states, read `references/ACCESSIBILITY.md` before finalizing.

## Required standards

Every response from this skill should aim to improve:

- first-glance clarity
- reading path
- perceived quality
- coherence between parts
- emotional tone
- implementation plausibility

Whenever useful, end with a short self-check against:
- Does the surface now have one main idea?
- Is the hierarchy visible at thumbnail, screen, and close-read distance?
- Is the structure felt even if the grid is invisible?
- Does the typography sound like the brand?
- Is color doing real work?
- What got removed?
- What remains too generic?

## Reference files — load on demand

Do not read every reference file on every activation. Load the one that matches the task.

- `references/LAWS.md` — the 22 operating laws. Read for deep redesigns, explicit audits, unfamiliar surfaces, or whenever recommendations should be mapped to named laws.
- `references/ENVIRONMENTS.md` — adaptation by surface type. Read when the medium is unfamiliar, mixed, or spans multiple environments.
- `references/OUTPUTS.md` — response formats and deliverables. Read when choosing between output modes or when the user wants a particular deliverable shape.
- `references/EVALUATION.md` — scorecard for audits and polish passes. Read only for QA, audit, acceptance, or final-review tasks.
- `references/ACCESSIBILITY.md` — accessibility floor for tasteful design. Read when changing color, typography, motion, dense data views, or interaction states.
- `references/FOUNDATIONS.md` — source records, design interpretations, and attribution limits. Read when the user asks why a principle exists or challenges the rationale.
- `references/FORMS.md` — optional intake prompts. Read only when context is genuinely too thin to proceed confidently.
