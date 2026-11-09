# Deneb Overview and Dataset Binding

Purpose: Host-level rules for Deneb visuals in Power BI, especially `dataset` binding, field naming, and row identity.

## Stable rules

- Treat Deneb as a Power BI host for Vega or Vega-Lite, not as a generic grammar sandbox.
- Bind report data through the named `dataset` source.
- In Vega-Lite, that usually means `"data": {"name": "dataset"}`.
- In raw Vega, that usually means a named data entry such as `{"name": "dataset"}` in the top-level `data` array.
- Reference fields by the display names exposed in the Values well, not blindly by model names.
- Expect Deneb to sanitize unsupported field characters such as `.`, `[`, `]`, `\`, and `"` when building dataset field names.
- Add only the columns and measures the visual actually needs; the Values well defines the dataset grain.
- Assume AppSource-certified Deneb visuals cannot fetch external data or resources.

## Common failure modes

- Forgetting the `dataset` binding entirely.
- Using the wrong field name because the Values-well display name or sanitization changed it.
- Adding extra fields and accidentally changing row grain or row count.
- Treating a transformed dataset as if it still has original row identity for interactivity.
- Assuming remote files, URLs, or external datasets are available in the certified visual.

## Safe defaults

- Start with the smallest Values-well shape and a minimal spec bound to `dataset`.
- Verify actual field names in editor autocomplete or the data pane before finalizing encodings or expressions.
- Default to Vega-Lite unless raw Vega is clearly necessary.
- Preserve original row context until the base chart and host interaction requirements are proven.
- Keep row-limit overrides out of the first working version unless you know the design needs them.

## Version caveats

- Verified against the stable Deneb docs surface available on 2026-03-26.
- Embedded Vega or Vega-Lite versions can lag upstream; check the editor status bar before using newer grammar features.
- PBIR persistence details live in `pbir-guide-1-9.md`, not here.

## Source URLs

- https://deneb.guide/docs
- https://deneb.guide/docs/dataset

## Verified version/date

- Stable Deneb introduction and dataset docs checked 2026-03-26.
