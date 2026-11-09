# Changelog

## 0.3.0 — 2026-09-09

- Consolidate three-lens adversarial review into Thermos; share scope and evidence verification. Preserve paired and single-lens behavior.

## 0.2.1 - 2026-08-24

- Added the portable Agent Plugins 1.0.0 manifest while retaining the Codex
  compatibility overlay.

## 0.2.0 - 2026-07-10

- Made Thermos use two ordinary same-wave native subagents with explicit
  correctness/security and maintainability contracts.
- Added context-free child starts where the host exposes `fork_turns`.
- Removed the sequential surrogate so Thermos never calls a non-parallel review
  a paired review.
- Clarified inherited permission behavior and added native-child smoke
  assertions.

## 0.1.0 - 2026-07-09

- Created the Codex-native, skills-only Thermos plugin.
- Added two parallel read-only review passes with one verified synthesis.
- Defined branch, pull-request, explicit-range, and dirty-worktree scope rules.
- Added an explicit parent-owned repair loop for `work until Thermos is happy`.
- Added skill metadata, OpenAI-backed design notes, and maintainer smoke cases.
- Pinned upstream attribution and preserved both MIT copyright notices.
