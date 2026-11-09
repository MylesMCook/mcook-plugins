# Changelog

## 0.2.1 - 2026-08-11

- Always save finished reports as Markdown files and return a clickable file
  link instead of duplicating the report body in chat.
- Define deterministic destination precedence, filename slugging, collision
  suffixes, update behavior, readback verification, and the no-chat-fallback
  rule.

## 0.2.0 - 2026-08-11

- Expand Bug Reporter from service wrappers to software, hardware, apps,
  infrastructure, data, build systems, and research tooling.
- Add distinct draft, investigation, improvement, formatting, and submission
  modes so report writing does not imply a live probe.
- Add exact reproduction rates, regression windows, minimal artifacts,
  fact-versus-inference labeling, honest missing-evidence handling, and
  agent-ready acceptance criteria.
- Add adaptive evidence guidance for crashes, performance, concurrency, data,
  UI and accessibility, builds, integrations, infrastructure, and private
  security disclosure.
- Replace the service-specific report form with a concise adaptive template and
  document the empirical and maintainer research basis.
- Make a finished Markdown file the default report artifact while preserving
  target tracker formats.
- Add an explicit concision gate against preambles, repeated facts, generic
  conclusions, empty boilerplate, and oversized artifact dumps.
- Keep hypotheses out of titles and summaries, require one highest-information
  next probe for incomplete reports, and avoid fabricated acceptance tests.
- Narrow activation to report and defect-handoff requests so ordinary bug-fix
  implementation work is not rerouted.
- Add a deterministic package and reporting-contract test gate.

## 0.1.0 - 2026-08-11

- Add an evidence-first workflow for API, MCP, connector, CLI, SDK, hosted
  service, and service-wrapper bug reports.
- Separate caller, configuration, upstream, wrapper-validation, state-safety,
  service, and documentation defects.
- Add guarded mutation tracing, confidential-data redaction, a reusable report
  template, fix direction, and acceptance-test requirements.
