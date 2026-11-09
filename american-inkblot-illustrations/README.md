# American Inkblot Illustrations

Make sparse, deadpan Inkblot illustrations without accidentally producing a
box-and-arrow hairball.

This skills-only plugin has two modes:

- **Inkblot-first** is the default for ordinary editorial, concept, article,
  and illustration requests. Inkblot is the main or only visible subject, with
  a nearly empty white canvas, few subordinate props, and no labels unless
  needed. Oversized props are explicitly rejected.
- **System portrait** is for explaining how a real system works. It inspects
  evidence, separates verified facts from inference, and turns only supported
  plumbing into a physical scene plus a truth ledger.

## What it produces

- Standalone 16:9 Inkblot-first art for everyday illustration work.
- Evidence-grounded system cutaways when the request is architectural or
  operational.
- One generated image at a time, checked before delivery.
- A bundled Inkblot visual reference for more consistent character shape and
  line style.

The image is an explanation, not an authoritative architecture record. Exact
ports, protocols, ownership, trust boundaries, and uncertainty stay in the
companion notes where they remain legible and reviewable.

## Use in Codex

```text
$american-inkblot-illustrations Illustrate this idea. Keep Inkblot as the main
or only subject, use no labels unless needed, and generate one image.
```

```text
$american-inkblot-illustrations Inspect this repository read-only, then show
one verified request path as a system portrait with a truth ledger.
```

```text
$american-inkblot-illustrations Plan three Inkblot-first body illustrations
for this essay. Do not generate yet.
```

When image generation is available, the skill generates one final image at a
time and checks it before moving on. Otherwise it returns ready-to-run prompts.

## Reliability contract

- Inspect before illustrating; do not invent topology to make a prettier scene.
- Default ambiguous requests to Inkblot-first instead of adding plumbing.
- Keep one audience, question, and abstraction level per plate.
- Mark facts as verified, inferred, or unknown outside the image.
- Put titles, scope, relationship details, and legends in the caption or notes,
  not inside the artwork.
- Use the bundled visual reference for final generation and style-sensitive
  edits when the host image tool supports reference images.

## Provenance

This plugin is an expanded marketplace edition of a local US English
localization inspired by Ian Xiaohei Illustrations. See
[ATTRIBUTION.md](ATTRIBUTION.md).

## License

MIT. See [LICENSE](LICENSE).
