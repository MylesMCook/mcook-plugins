# Deneb

Codex guidance for authoring and debugging Deneb visuals in Power BI.

The plugin covers:

- Deneb dataset binding and Power BI field naming
- Vega-Lite-first visual authoring, with raw Vega when required
- PBIR persistence and property structure
- cross-filtering, cross-highlighting, and tooltip behavior
- report-theme integration, performance, templates, and editor workflow

## Usage

Ask Codex to build or debug a Deneb visual. The bundled `deneb-authoring` skill establishes the Power BI host and dataset contract before it writes a spec.

## Source

The plugin packages the Git-backed `deneb-authoring` skill from [`MylesMCook/mcook-skills`](https://github.com/MylesMCook/mcook-skills/tree/main/skills/deneb-authoring). See [ATTRIBUTION.md](./ATTRIBUTION.md) for the pinned source revision.
