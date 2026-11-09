---
name: deneb-authoring
description: Author and debug Deneb visuals for Power BI, including dataset binding, PBIR persistence, report-theme integration, interactivity, and template metadata. Use this first for Deneb, Power BI, PBIR, report-theme, cross-filter, cross-highlight, or dataset-binding requests. Start with host constraints, default to Vega-Lite, and switch to raw Vega only when the requirement clearly needs lower-level control.
---

# Deneb Authoring

Use this skill for Deneb in Power BI: dataset binding, PBIR, templates, interactivity, theme alignment, and editor workflow.

## Use when

- The task is about Deneb, Power BI, PBIR, report-theme integration, dataset binding, template metadata, or Deneb interactivity.
- You need to author or debug a Vega or Vega-Lite visual that must run inside Deneb.
- The request mentions cross-filtering, cross-highlighting, Power BI tooltips, report themes, or editor workflow in Deneb.

## Do not use when

- The task is plain Vega or plain Vega-Lite work outside Deneb and Power BI.
- The user only needs generic chart grammar advice with no Deneb host constraints.
- The requirement is a host-agnostic Vega or Vega-Lite example that should not be shaped by Power BI behavior.

## Precedence / handoff

- This skill leads for Deneb and Power BI visual work, even when the embedded grammar is Vega or Vega-Lite.
- Lock host constraints first: `dataset` binding, row identity, external-resource limits, interactivity implications, runtime/version caveats, and PBIR persistence rules.
- Default to Vega-Lite after host constraints are clear.
- Switch to raw Vega only when Vega-Lite cannot express the required behavior cleanly, especially for lower-level signal or event-stream work.

## Required reasoning steps

1. Confirm the Deneb host context, provider choice, and whether PBIR or template metadata is involved.
2. Lock the `dataset` contract, actual field/display names, and any field sanitization concerns before writing encodings.
3. Identify whether interactivity depends on preserving row identity and call out transforms or aggregation that could break reconciliation.
4. Choose Vega-Lite by default; escalate to raw Vega only when the requirement justifies it.
5. Produce the smallest working Deneb-ready spec or PBIR payload first, then add optional interactivity, theme integration, or template metadata.

## Output contract

Always return:

- the chosen grammar and why
- assumptions about host context, data shape, field names, and provider/runtime
- a minimal working Deneb-ready spec first
- optional refinements separately
- version caveats when Deneb's embedded runtime or PBIR behavior may lag upstream docs
- likely host-specific risks
- the next debugging step if the first attempt fails

## Version policy

- Prefer stable Deneb docs over canary or `next` docs.
- Pin PBIR guidance in this skill to the stable 1.9 line for this pass.
- Treat Deneb's embedded Vega or Vega-Lite runtime as authoritative over upstream grammar docs when features conflict.
- Keep copied reference text short and curated; do not mirror large doc pages.

## Known failure modes

- Forgetting to bind `dataset` or using the wrong field names from the Values well.
- Mutating or aggregating data in ways that break row reconciliation for Power BI interactivity.
- Assuming certified Deneb visuals can fetch external resources.
- Using upstream Vega or Vega-Lite features that are newer than Deneb's embedded runtime.
- Mixing plain Vega or Vega-Lite template JSON with Deneb template metadata rules.

## Load references

- Load `references/overview-and-dataset.md` first for dataset binding, field naming, and host constraints.
- Load `references/editor-workflow.md` for advanced editor workflow, provider switching, debug panes, and runtime/version checks.
- Load `references/interactivity.md` when selection, highlight, tooltips, or row reconciliation matter.
- Load `references/performance-and-theme.md` when row limits, renderer choice, or report-theme integration matter.
- Load `references/pbir-guide-1-9.md` for PBIR persistence and property structure.
- Load `references/template-structure.md` for Deneb template metadata shape.
- Load `references/templates-and-usermeta.md` when importing, exporting, or adapting templates.
