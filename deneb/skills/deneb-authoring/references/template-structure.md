# Deneb Template Structure

Purpose: Compact structure guidance for Deneb template metadata.

## Stable rules

- A Deneb template is still a Vega or Vega-Lite spec at the top level.
- Deneb-specific template metadata lives inside `usermeta`.
- `usermeta` must contain the child objects `deneb`, `information`, and `dataset` for a valid Deneb template.
- `usermeta.deneb` carries template metadata version and provider identity.
- `usermeta.information` carries human-facing template metadata such as name and description.
- `usermeta.dataset` carries placeholder metadata for fields the importing user must map.

## Common failure modes

- Treating a plain Vega or Vega-Lite example as if it were already a valid Deneb template.
- Omitting required metadata objects inside `usermeta`.
- Setting the wrong provider or inconsistent provider metadata.
- Leaving dataset placeholders ambiguous or overly tied to one report's exact field layout.
- Mixing template metadata concerns with the runtime spec itself.

## Safe defaults

- Keep the top-level spec valid on its own before adding Deneb template metadata.
- Set provider metadata to match the actual spec grammar.
- Keep placeholder names human-readable and aligned with what the importer must choose.
- Keep template metadata concise and portable.
- Use the Deneb template schema as a validation aid, not as the primary authoring surface.

## Version caveats

- This guidance is for the Deneb template metadata format currently used by stable docs.
- Template compatibility can vary across older Deneb lines, especially for field-name limits and newer metadata affordances.

## Source URLs

- https://deneb.guide/docs/templates
- https://deneb-viz.github.io/schema/deneb-template-usermeta-v1.json

## Verified version/date

- Stable Deneb template docs and template schema checked 2026-03-26.
