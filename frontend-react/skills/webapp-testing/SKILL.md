---
name: webapp-testing
description: Verify local web applications with Playwright CLI for live browser work and the repository's existing test runner for durable regressions. Use for UI flows, screenshots, console errors, accessibility checks, and browser debugging.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

## Codex compatibility

Honor the target repository's instructions and existing test stack. For live browser work, use the installed official Playwright skill and its `playwright-cli` workflow. Do not install browser tooling or dependencies without authorization. Use another browser tool only when the user requests it or Playwright CLI lacks a required capability.

### Choose the browser path

Use the smallest path that produces the evidence the user needs:

- **Live verification or exploratory debugging:** use Playwright CLI with an isolated named session. Take a snapshot before using element references and refresh it after navigation or meaningful UI changes. Capture screenshots, traces, and console evidence when they answer the task. Close the session you own.
- **Durable regression or CI coverage:** use the repository's committed browser-test runner, configuration, language, and dependencies. Extend an existing Playwright suite when it fits; do not introduce a parallel Python harness.
- **React runtime diagnosis:** reproduce the affected flow in Playwright CLI, then use the project's existing profiling or diagnostic tools for render counts and Web Vitals. Report measurements only when observed; a screenshot does not establish runtime performance.
- **Formal QA handoff:** use Playwright CLI to collect reproducible steps, targeted screenshots or traces, and a concise issue report. Verify each issue in the running app before reporting it.

Keep exploration and committed regression tests distinct: a successful browser click does not replace an assertion in the project's test suite.

### Annotation-mode check

Playwright can verify the application, but it does not prove that Codex annotation mode works in the in-app browser. If annotation mode hides the pointer, shows a small black box, or cannot select an element while ordinary interaction still works, check for a collision between the page's style CSP and Codex's injected annotation stylesheet before clearing browser state or changing application CSS. Read [Diagnose Codex annotation CSP failures](references/codex-annotation-csp.md). When annotation mode works normally, do not change the application's CSP.

## Bundled legacy helper

The upstream Python examples and `scripts/with_server.py` remain in the package for existing consumers. Use them only when explicitly requested or when Playwright CLI cannot provide a required capability. Inspect the helper's `--help` before use. Wait for the specific UI state or assertion needed; do not treat `networkidle` or fixed timeouts as proof that a page is ready.
