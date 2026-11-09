# Changelog

## 0.1.1 - 2026-08-24

- Added the portable Agent Plugins 1.0.0 manifest while retaining the Codex
  compatibility overlay.

## Unreleased

- Bundle the Goalie skill and its Codex metadata with the marketplace plugin.
- Make the optional brrr Stop hook portable to Windows with `py -3`.
- Keep Goal drafting independent from notification configuration.

## 0.1.0

- Package the Goalie skill as a Codex plugin.
- Add a quiet brrr Stop hook for blocked Goal and needs-attention notifications.
- Add deterministic hook tests.
- Keep the notification hook quiet and deterministic.
