# Changelog

## 0.3.2 - 2026-11-08

- Add an explicit Claude manifest for claude.ai marketplace synchronization.

## 0.3.1

- Made Playwright CLI the live browser default and retained repository-native browser tests for regressions.
- Removed agent-browser routing and stale Python examples from the testing skill; kept the bundled server helper for existing consumers.

## 0.3.0

- Added three commit-pinned skills discovered through UI Skills MCP for accessibility, motion performance, and page metadata.
- Added Codex metadata, source attribution, and deterministic upstream refresh support for those skills.

## 0.2.2 — 2026-09-09

- Add framework ownership and Next.js compatibility boundaries to React guidance and its upstream sync overlay.

## 0.2.1

- Made the plugin repository authoritative for Base UI + StyleX, alongside StyleX.
- Removed the incoming mcook-skills sync and pin; retained historical attribution.
- Documented the standalone copy as an optional outward export and verified that upstream sync preserves plugin-owned edits.

## 0.2.0

- Added commit-pinned Base UI + StyleX guidance maintained in mcook-skills.
- Separated component integration from general StyleX work and narrowed shadcn routing in mixed projects.
- Required current official documentation, version matching, and direct supporting citations in both styling skills.
- Added selective upstream refresh and locked reproduction, routing evaluations, and a compiled interactive dialog evaluation.

## 0.1.3

- Added an optional agent-browser path for live verification, React runtime diagnostics, Web
  Vitals, accessibility audits, and formal dogfood reports.
- Kept repository-native Playwright as the durable regression and CI path, with the bundled Python
  helper as an authorized fallback.
- Added browser-path trigger and output evals, preserved by the deterministic upstream sync overlay.

## 0.1.2

- Refreshed `vercel-labs-agent-skills` from `dd089a8c752c` to `20e89cc4bb25`.
- Refreshed `shadcn-ui` from `b9938d94635f` to `683a5a9b370a`.
- Refreshed `wshobson-agents` from `d82998e7df39` to `38e19c20d2b1`.

## 0.1.1

- Added a strict-CSP diagnostic for Codex annotation failures without recommending broad style-policy relaxation.

## 0.1.0

- Added five pinned React, shadcn/ui, Playwright, and TypeScript skills plus a Codex-native StyleX skill.
- Added exact upstream commit pins and deterministic Codex compatibility transforms.
- Added a weekly pull-request workflow for reviewable upstream refreshes.
