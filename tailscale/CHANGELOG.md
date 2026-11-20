# Changelog

## 0.2.0 - 2026-11-20

- Make the skill docs-first: local CLI help, then the live page as Markdown,
  then `docs/llms.txt`, with deprecation and "Last validated" checks.
- Rename Border0 to Tailscale PAM (`references/pam.md`) from current docs.
- Add references for Tailscale Services and route selection (MagicRoute),
  credentials (trust credentials, workload identity, OAuth apps) and tsidp,
  and a documentation map covering every docs section and feature page.
- Add newer Aperture pages (chat, skills, model aliases, token purchasing).
- Replace host-specific tool names with host-neutral wording.
- Add `scripts/check_freshness.py` and a weekly freshness workflow.

## 0.1.1 - 2026-11-08

- Add an explicit Claude manifest for claude.ai marketplace synchronization.

## 0.1.0 - 2026-10-10

- Package the upstream Tailscale skill and all 17 references as one plugin.
- Preserve the BSD-3-Clause license and pinned source attribution.
- Add portable and OpenAI manifests, skill UI metadata, and marketplace entries.
- Adapt entrypoint triggers, tool wording, and operating boundaries.
