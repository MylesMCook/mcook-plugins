---
name: american-inkblot-illustrations
description: >-
  Create, plan, prompt, edit, and QA sparse 16:9 US English illustrations with
  Inkblot, a small solid-black deadpan worker. Use when the user asks for
  Inkblot or American Inkblot style, sparse white-background hand-drawn
  editorial/concept/article art, or a friendly visual explanation of software,
  services, agents, automations, homelabs, and operational systems. Default
  eligible non-system requests to Inkblot-first art: Inkblot is the main or
  only visible subject, with few props and no labels unless needed. Use an
  evidence-grounded system portrait for real system plumbing, handoffs, state,
  trust boundaries, failure, and recovery. Do not use for exact compliance or
  network diagrams, authoritative topology, quantitative charts, polished
  brand art, slide decks, logos, memes, children's cartoons, or unrelated
  generic image prompts.
---

# American Inkblot Illustrations

Turn one important truth about a system or article into a sparse, memorable,
weird-but-clear hand-drawn scene. Make Inkblot, a small solid-black deadpan
worker with white dot eyes and thin legs, perform the conceptual work.

## Choose one mode

| Mode | Use when | Default composition |
|---|---|---|
| **Inkblot-first** | Editorial, concept, metaphor, article art, or a general Inkblot request | One Inkblot as the main or only visible subject, 0-2 essential props, no labels unless needed |
| **System portrait** | Explaining how a real or supplied system works | One physical scene with 3-6 verified elements plus a companion truth ledger |

If the request is ambiguous, use Inkblot-first. Do not add plumbing, labels, or
explainer machinery merely because the skill can make system portraits.

## Hold the truth boundary

For a system portrait, treat the illustration as an explanatory view, never as
the authoritative system record. Inspect available evidence before drawing.
Do not invent a component, relationship, protocol, trust boundary, failure
path, or runtime state to improve the composition.

Keep exact scope, relationships, technologies, and uncertainty in a companion
truth ledger outside the image. Mark claims as:

- `[verified]` directly supported by inspected evidence.
- `[inferred]` strongly suggested but not directly observed.
- `[unknown]` missing or contradictory.

If an unknown changes the meaning of the plate, omit it from the image or show
an intentionally unresolved edge and state the question outside the image.

## Load only the needed reference

| Situation | Load |
|---|---|
| Mapping a real system, choosing zoom, or handling evidence and uncertainty | `references/system-portrait-method.md` |
| Style fidelity or image generation/editing matters | `references/style-dna.md` |
| Inkblot's shape, role, or action might drift | `references/inkblot-mascot.md` |
| Choosing a plate structure or inventing a physical metaphor | `references/composition-patterns.md` |
| Writing a final image prompt or calling an image tool | `references/prompt-template.md` |
| Reviewing a plan, generated image, or edit | `references/qa-checklist.md` |
| Needing short US English labels | `assets/label-bank.md` |
| Needing the research basis for the method | `references/research-foundations.md` |

For every final generation or style-sensitive edit, inspect
`assets/inkblot-reference.png` and pass it to the host image tool as a character
and line-style reference when supported. Do not reproduce its three-pose
layout; it is a consistency reference, not a composition template.

Do not preload every reference.

## Workflow

1. **Resolve the mode and deliverable.** Choose Inkblot-first or system
   portrait, then decide whether the user wants a plan, prompt, final image, or
   narrow edit.
2. **Ground only what needs grounding.** For Inkblot-first art, use the supplied
   idea or article. For a system portrait, inspect the smallest useful set of
   source, config, manifests, logs, screenshots, or current documentation.
   Keep inspection read-only unless the user asked for changes. Never restart a
   service merely to illustrate it.
3. **Build only the needed brief.** For Inkblot-first, state one core idea and
   one physical action. For a system portrait, declare runtime-grounded,
   configuration-grounded, or conceptual and record material sources and
   unknowns.
4. **Keep one idea and one zoom.** For a system portrait, keep one abstraction level
   per plate. Split the story instead of mixing levels.
5. **Use the smallest useful set.** Default to one image. Use extra images only
   when each answers a different question; never exceed five system plates or
   nine article shots.
6. **Generate one image at a time.** Load `references/prompt-template.md` and
   use the host image-generation tool when available; otherwise return the
   final prompt. Do not make a collage unless the user asks for a comic strip.
7. **QA before delivery.** Check factual fidelity when applicable, then visual
   fidelity with `references/qa-checklist.md`. Regenerate or narrowly edit a
   failed image.
8. **Deliver simply.** Return the picture plus a short caption. Add a truth
   ledger only for system portraits or when factual uncertainty matters.

## System portrait plan

Use this compact table:

| Plate | Audience question | Zoom | Structure | Core truth | Inkblot action | Evidence | Labels |
|---|---|---|---|---|---|---|---|

After the table, add only the material truth ledger:

```text
Scope:
Verified:
Inferred:
Unknown:
Exact relationships:
Sources inspected:
```

Keep relationship wording directional and specific: `proxy forwards HTTPS to
app on 127.0.0.1:8484`, not `proxy uses app`.

## Article shot list

Use the existing editorial format:

| Placement | Theme | Core idea | Structure | Inkblot action | Elements | Labels |
|---|---|---|---|---|---|---|

Pick cognitive anchors rather than paragraphs: decisions, bottlenecks,
before/after contrasts, evidence chains, trust gaps, handoffs, tradeoffs,
feedback loops, and stuck-to-running state changes.

## Visual defaults

- Use a standalone 16:9 horizontal composition on pure white.
- Use black, slightly wobbly thin line art.
- Use orange for the primary path or handoff, red for failure/friction/risk,
  and blue for state, feedback, secondary context, or an unresolved edge.
- Keep Inkblot central to the mechanism, serious about a strange job, and not
  cute, human, racialized, gendered, patriotic, polished, or logo-like.
- Keep the in-image canvas title-free. Put the plate title and scope in the
  caption or filename.

**Inkblot-first defaults:** at least 50% empty space, one Inkblot, 0-2 essential
props, and 0-3 short labels only when words materially help. Inkblot should be
the visual focal point; no prop may be larger or more prominent. Do not add
system plumbing by default. Never describe or draw an oversized prop in this
mode.

**System-portrait defaults:** at least 35% empty space, roughly 3-6 verified
elements, and up to five short labels only when needed. Represent relationships with one
physical scene—pipes, cables, trays, doors, relays, parcels, reservoirs, or a
repair bench—not boxes wearing a hand-drawn costume.

## Save workspace output

Resolve a writable output root before generation: use an explicit user path
first, otherwise the current project/workspace root. If neither exists, return
the images or prompts in the conversation and ask for a destination only when
durable files are required. Never write generated output into the installed
plugin or skill directory.

For a system portrait, save under
`<workspace-root>/assets/<system-slug>-system-portrait/` as `01-context.png`,
`02-plumbing.png`, and focused names such as `03-failure-recovery.png`. Save the
truth ledger as `system-notes.md` when the user wants durable artifacts.

For article body art, save under
`<workspace-root>/assets/<article-slug>-illustrations/` as `01-topic-name.png`,
`02-topic-name.png`, and so on.

Do not overwrite existing assets unless asked.

## Stop conditions

- If the user needs an exact editable architecture, network, compliance,
  threat-model, or quantitative artifact, use the appropriate diagramming or
  data-visualization workflow and offer Inkblot only as a companion explainer.
- If source evidence is unavailable but a concept is clear, label the result a
  conceptual portrait and do not imply that it reflects live topology.
- If generated text is wrong, reduce or remove in-image labels and keep the
  exact wording in the caption.
