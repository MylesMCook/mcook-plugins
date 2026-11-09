# Image Prompt Template

Load this when writing a final prompt, calling an image-generation tool, or
editing a generated image. Replace every brace and remove irrelevant lines.
Use one prompt per final illustration.

## Contents

- Inkblot-first prompt
- System portrait prompt
- Editorial prompt
- Edit prompts

Before final generation or any edit that may redraw Inkblot, inspect
`../assets/inkblot-reference.png` and pass it to the image tool as a character
and line-style reference when supported. Use the reference's Inkblot shape and
tone, not its three-pose layout.

## Inkblot-first prompt

```text
Generate one standalone 16:9 horizontal US English editorial illustration.

Core idea:
{one sentence the viewer should understand}

Inkblot action:
{one strange physical action that carries the idea}

Essential props:
{zero, one, or two objects; use none when Inkblot alone is enough}

Exact in-image labels, and no other text:
{normally "none"; otherwise up to three labels of 1-3 words each}

Use the supplied Inkblot visual reference for character shape and line style,
but create one new composition. Show one small solid-black abstract Inkblot
worker with white dot eyes, tiny thin limbs, a blank serious expression, and a
slightly uneven outline. Inkblot is the main or only visible subject and
performs the core action. Inkblot is the visual focal point. Every prop is
smaller and less prominent than Inkblot; use the reference for appearance, not
character scale. Never use an oversized prop or make an object loom over
Inkblot.

Pure white background. Thin, slightly wobbly black hand-drawn line art. At
least 50% empty space. Use orange, red, or blue only for one meaningful accent.
No background machinery, extra characters, title, diagram, grid, realistic UI,
scenery, texture, beige, shadow, gradient, polished vector style, cute mascot
pose, clothing, human features, logo treatment, or watermark.
```

## System portrait prompt

```text
Generate one standalone 16:9 horizontal editorial illustration that explains
one verified aspect of a real system.

Purpose and audience:
{what this plate should help whom understand}

Plate title and scope, for context only; do not draw this title:
{external caption title} / {one abstraction level and boundary}

System truth to visualize:
{3-6 verified elements and one specific primary relationship or behavior}

Do not visualize as fact:
{inferred or unknown elements to omit, generalize, or show as unresolved}

Physical composition:
{one selected pattern, object placement, primary path, state, boundary, and Inkblot action}

Exact in-image labels, and no other text:
{normally "none"; otherwise up to five labels of 1-3 words each}

Visual DNA:
Pure white background. Minimalist black hand-drawn line art with slightly
wobbly thin pen lines and at least 35% empty space. Sparse orange, red, and blue
handwritten American English notes. The main subject covers roughly 40%-60% of
the canvas. One physical scene, not a formal diagram.

Inkblot:
A small solid-black abstract blob worker with white dot eyes, tiny thin legs, a
blank serious expression, and a slightly uneven outline. Inkblot performs the
core system action. Inkblot is deadpan and useful; not human, racialized,
gendered, cute, glossy, heroic, or logo-like.

Use the supplied Inkblot visual reference for character shape and line style,
but do not copy its three-pose layout.

Color semantics:
Black for structure and objects. Orange only for the primary request, payload,
route, or handoff. Red only for a failure, alarm, friction, risk, or important
result. Blue only for state, feedback, secondary context, or an intentionally
unresolved edge. Meaning must remain clear without color.

Hard constraints:
Preserve the stated direction, state, ownership, boundary, and failure
semantics. Do not invent components or connections. Do not include a title,
legend, protocol paragraph, port number, secret, code, realistic UI, cloud-icon
wall, grid, swim lane, architecture boxes, dense arrows, PPT infographic,
paper texture, beige background, gradient, shadow, scenery, patriotic imagery,
or copied source-project composition.

The result should feel like a strange cutaway workshop or repair-manual doodle:
friendly at first glance, technically honest on inspection.
```

## Editorial prompt

Use the Inkblot-first prompt unless the user explicitly needs a structured
multi-element editorial explainer. For that exception, use:

```text
Generate one standalone 16:9 horizontal US English article body illustration.

Core idea:
{one sentence the reader should understand}

Structure and composition:
{one editorial pattern, specific low-tech metaphor, and Inkblot action}

Exact in-image labels, and no other text:
{normally "none"; otherwise up to three labels of 1-3 words each}

Use a pure white background, thin slightly wobbly black hand-drawn line art,
at least 50% empty space, and restrained orange/red/blue notes. Inkblot is a
small solid-black abstract worker with white dot eyes and thin legs. Inkblot
must perform the central conceptual action and must not look cute, human,
racialized, gendered, patriotic, polished, or logo-like.

One image explains one idea. Do not add a title, sentences, a grid, formal
flowchart, realistic UI, PPT layout, paper texture, beige, shadow, gradient,
complex scenery, or a copied example composition.
```

## Edit prompts

When an edit may redraw Inkblot, include the supplied reference image and state
that Inkblot's body, eyes, limbs, line style, and deadpan tone must remain
consistent.

### Remove accidental title

```text
Edit the provided image. Remove only the handwritten title "{text}" and its
underline or title mark. Fill that area with the same pure white background.
Preserve Inkblot, labels, paths, line style, composition, aspect ratio, and
quality. Do not add text or objects.
```

### Correct factual direction

```text
Edit the provided image while preserving its style and layout. Correct only
the primary orange path so it travels from {origin} to {destination} and shows
{specific action or payload}. Keep all other verified objects unchanged. Do
not add components, labels, title text, or decorative arrows.
```

### Make Inkblot causal

```text
Regenerate the same verified system truth and simple layout, but make Inkblot
perform {core action}. Removing Inkblot should make the mechanism stop working.
Keep the result sparse, deadpan, hand-drawn, and not cute.
```

### Reduce text and diagram energy

```text
Regenerate the same verified system truth as one physical scene. Remove the
title, grid, architecture boxes, most arrows, protocol prose, and sentence-
length labels. For Inkblot-first art, keep 0-3 short labels; for a system
portrait, keep 0-5 short labels according to actual need: {labels}. Preserve
the primary direction, state, boundary, and Inkblot action.
```
