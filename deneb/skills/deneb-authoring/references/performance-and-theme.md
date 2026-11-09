# Deneb Performance and Theme

Purpose: Deneb-specific rules for row limits, field selection, renderer tradeoffs, and Power BI theme integration.

## Stable rules

- Deneb caps rows at 10,000 by default unless the row-limit override is enabled.
- Add only the columns and measures the visual actually needs; extra fields can change grain, row count, and performance.
- Editing large datasets in the advanced editor has real performance costs.
- Renderer choice matters: SVG and Canvas have different tradeoffs for complexity and interaction.
- Use Power BI theme integration intentionally through `pbiColor` and the `pbiColor*` schemes when theme fidelity matters.

## Common failure modes

- Assuming the visual has the full underlying dataset when the row cap is in play.
- Adding convenience fields that accidentally change row grain or dataset size.
- Leaving auto-apply on while editing large datasets, then blaming the grammar.
- Using ordinal theme schemes without considering category count and wraparound behavior.
- Hard-coding colors when the visual should follow the report theme.

## Safe defaults

- Start under the default row limit and only override it when the design truly requires more rows.
- Keep the Values well minimal until the chart and interaction model are proven.
- Use Vega-Lite first because it usually reaches a working result faster.
- Prefer report-theme helpers when the visual should stay aligned with Power BI theme changes.
- Check the data pane and performance symptoms before optimizing the spec itself.

## Version caveats

- Theme helpers and scheme behavior follow the active Deneb runtime.
- Performance depends on both Deneb version and report context; editor behavior can differ from steady-state report rendering.

## Source URLs

- https://deneb.guide/docs/dataset
- https://deneb.guide/docs/performance
- https://deneb.guide/docs/schemes

## Verified version/date

- Deneb stable dataset, performance, and theme docs checked 2026-03-26.
