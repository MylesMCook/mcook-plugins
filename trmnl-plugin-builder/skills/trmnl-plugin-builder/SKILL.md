---
name: trmnl-plugin-builder
description: Plan and operate Myles Cook's TRMNL plugins alongside TRMNL's official skill. Use for plugin-path and data-strategy decisions, secret boundaries, infrastructure, hosted-action approvals, rollout, and evidence. Do not use for ordinary TRMNL markup or layout work alone.
license: MIT
---

# TRMNL Operations Companion

Use this skill with TRMNL's official `trmnl` skill. The official skill and
hosted MCP own current product, Liquid, Framework, design-system, and API
guidance. This companion owns Myles-specific architecture and operational
boundaries.

## Start here

- Load the official `trmnl` skill for any markup, layout, Framework, recipe, or
  hosted-plugin work. If it is unavailable, use live official TRMNL docs and
  say that the official skill was unavailable.
- Read [official-tooling.md](references/official-tooling.md) when setting up or
  choosing agent/LLM tooling.
- Read [source-policy.md](references/source-policy.md) before implementation.
- Never place provider or TRMNL secrets in fields, preview data, docs, sample
  payloads, generated artifacts, commands, or logs.
- Do not write to TRMNL, refresh, capture screenshots, publish, deploy, or
  inspect a device without explicit approval for that action. Read
  [hosted-actions-and-verification.md](references/hosted-actions-and-verification.md).
- Do not add a custom agent, MCP server, app, or unrelated runtime surface
  unless the task cannot work without it and the user approves that scope.

## Companion workflow

1. Classify the request with
   [decisions-and-data.md](references/decisions-and-data.md). Use a Private
   Plugin unless its requirements genuinely demand another path.
2. Use the official `trmnl` skill and current official sources for product,
   markup, Framework, template, and hosted MCP decisions.
3. Design the smallest data contract and a synthetic, non-sensitive fixture.
   Choose polling, webhook, or Plugin Merge from the actual data flow.
4. Read [markup-fields-and-artifacts.md](references/markup-fields-and-artifacts.md)
   for the companion's safety and artifact boundaries. Defer syntax and design
   rules to the official skill and current docs.
5. State exactly what an offline preview proves and what it does not. A local
   render never proves hosted merge variables, hosted refresh behavior, or a
   physical device.
6. Present the proposed hosted operations and wait for approval. After an
   approved operation, verify the narrowest affected behavior and report the
   remaining boundary.

## Path choice

- **Private Plugin:** normal default for a personal/private screen.
- **Recipe:** use only when a Private Plugin should become a shareable TRMNL
  artifact and its sanitized preview/publication behavior is acceptable.
- **Third Party:** use only for a public server-backed integration with OAuth,
  author-managed user data, or a custom management flow.
- **BYOS:** use only to own the server/device relationship, not to make a
  normal hosted plugin.
