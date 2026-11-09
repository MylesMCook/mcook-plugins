# Deneb Interactivity

Purpose: Host-specific guidance for selection, highlight, tooltip, and row-reconciliation behavior in Deneb.

## Stable rules

- Deneb interactivity depends on Power BI being able to reconcile the rendered datum back to original dataset rows.
- If a mark still reflects the original dataset row context, Power BI can support tooltip, drill-through, cross-filter, and highlight behavior more reliably.
- Deneb adds reconciliation fields such as `__row__` and `__selected__` when row identity is preserved.
- Cross-highlighting adds measure-specific helper fields such as `__highlight`, `__highlightStatus`, and `__highlightComparator`.
- Host interactivity constraints matter as much as grammar syntax.

## Common failure modes

- Applying transforms, aggregation, or reshaping that break row identity and then expecting Power BI cross-filter behavior to keep working.
- Treating a derived row or aggregate mark as if it still maps one-to-one to a source row.
- Debugging tooltip or selection behavior without inspecting the actual datum Deneb produced.
- Designing the visual effect for selection first and ignoring whether Power BI can resolve the row context at all.

## Safe defaults

- Preserve original row context until you have proven the base interaction requirement.
- When interactivity matters, avoid unnecessary transforms on the primary `dataset`.
- Inspect the data pane or datum tooltips to verify whether reconciliation fields are still present.
- Treat aggregate or transformed views as higher risk for Power BI interaction unless you have a deliberate workaround.
- Debug host reconciliation first, then debug the visual styling of selected or highlighted states.

## Version caveats

- Interactivity behavior depends on both Deneb and Power BI host behavior.
- Embedded Vega and Vega-Lite logic can influence how derived rows behave, but Power BI reconciliation is the hard constraint.

## Source URLs

- https://deneb.guide/docs/interactivity-overview

## Verified version/date

- Stable Deneb interactivity overview checked 2026-03-26.
