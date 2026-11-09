# Deneb Editor Workflow

Purpose: Stable advanced-editor workflow guidance for authoring, debugging, and checking embedded runtime behavior.

## Stable rules

- The editor is only available in report edit mode and only after the visual has data in the Values role.
- Treat the editor as the source of truth for the active provider and embedded Vega or Vega-Lite version.
- Apply changes deliberately; auto-apply is convenient but can be expensive on larger datasets.
- Use the data, signals, and logs panes to debug what Deneb actually parsed, not what you expected.
- Check the editor status bar before relying on upstream Vega or Vega-Lite features.

## Common failure modes

- Debugging against upstream docs without checking the embedded runtime version.
- Leaving auto-apply on while working with large datasets and mistaking performance pain for spec failure.
- Exiting the editor with unapplied changes.
- Debugging only the rendered chart and ignoring the data or signals panes.
- Switching providers without reconciling the spec shape.

## Safe defaults

- Start with Vega-Lite unless the requirement clearly needs raw Vega.
- Work with apply-first editing on larger datasets; use auto-apply only when iteration speed matters more than cost.
- Validate field names and dataset shape in the data pane before rewriting encodings.
- Use the logs pane when parsing succeeds but behavior is still wrong.
- Reconfirm the active provider after opening imported or generated content.

## Version caveats

- The embedded Vega or Vega-Lite runtime can lag upstream releases.
- Editor affordances can change across Deneb versions; treat the current stable docs and the live editor as authoritative.

## Source URLs

- https://deneb.guide/docs/visual-editor

## Verified version/date

- Deneb stable visual editor docs checked 2026-03-26.
