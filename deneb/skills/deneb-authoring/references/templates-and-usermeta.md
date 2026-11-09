# Deneb Templates and Usermeta

Purpose: Practical rules for importing, exporting, and adapting Deneb templates without confusing them with plain Vega or Vega-Lite specs.

## Stable rules

- Deneb can import existing templates from the create-new-specification flow; template import is part of the current stable docs.
- Only valid Deneb templates import directly. Plain Vega or Vega-Lite examples usually need either editor paste-in or added template metadata.
- Template metadata lives in `usermeta`; see `template-structure.md` for the exact shape.
- Template placeholders are driven by the dataset metadata captured at export time.
- Keep the source dataset minimal when exporting a template so placeholder intent stays clear and row grain stays portable.
- Preview images are optional and can leak sensitive visual information.

## Common failure modes

- Treating any Vega or Vega-Lite example as importable without Deneb metadata.
- Exporting templates with superfluous dataset fields and making import mapping ambiguous.
- Leaving placeholder names too specific to one report or too vague to be useful.
- Including preview images when the report content is sensitive.
- Forgetting that columns and measures are not interchangeable when mapping placeholders.

## Safe defaults

- For an external Vega or Vega-Lite example, start from an empty Deneb spec and paste the grammar first unless you are intentionally building a reusable Deneb template.
- Keep template placeholders specific enough to guide mapping, but general enough to reuse across reports.
- Remove unneeded fields from the Values well before exporting a template.
- Skip preview images unless there is a clear benefit and the data is safe to expose.
- Use copy-to-clipboard export when direct download is unavailable in the tenant.

## Version caveats

- Template import and export behavior follows the current stable Deneb docs checked on 2026-03-26.
- Template compatibility can vary across older Deneb lines, especially around field-name constraints and metadata evolution.

## Source URLs

- https://deneb.guide/docs/templates
- https://deneb-viz.github.io/schema/deneb-template-usermeta-v1.json

## Verified version/date

- Stable Deneb template docs and template schema checked 2026-03-26.
