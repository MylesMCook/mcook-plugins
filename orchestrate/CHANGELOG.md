# Changelog

## 0.2.0 - 2026-11-13

- Make the skill host-neutral: works with any host's native subagent tools (Codex, Claude Code, Factory Droid) and routes by capability tier with per-host model examples.

## 0.1.4 - 2026-11-08

- Add an explicit Claude manifest for claude.ai marketplace synchronization.

## 0.1.3 - 2026-08-27

- Require explicit Orchestrate activation instead of treating task size as
  permission to delegate.
- Gate on native subagent spawn and supervision tools rather than an internal
  release label.
- Record observed history mode in routing evidence when the host exposes it.
- Add regression coverage for implicit activation and capability detection.

## 0.1.2 - 2026-08-24

- Added the portable Agent Plugins 1.0.0 manifest while retaining the Codex
  compatibility overlay.

## 0.1.1 - 2026-07-27

- Restrict the workflow to the native Codex subagent surface with no legacy
  fallback.
- Align model routing with current GPT-5.6 and Codex-Spark guidance.
- Record runtime routing evidence only when the parent can observe it, and
  distinguish it from configuration-derived expectations.
- Clarify concurrency as a local policy and delegation as coordination rather
  than sandbox or permission isolation.
- Keep Responses API multi-agent implementations outside this native-Codex
  workflow.

## 0.1.0 - 2026-07-11

- Add a Codex-native orchestration workflow with deliberate model routing.
- Add bounded concurrency, write ownership, structured handoffs, and routing
  verification.
- Keep v1 skills-only with no external runtime or API dependency.
