# TRMNL Operations Companion

A thin Myles-specific companion to TRMNL's official agent skill and hosted MCP.
TRMNL's maintained tooling owns markup, Framework, design-system, API, and
hosted-plugin guidance. This package keeps local architecture, secret, approval,
rollout, and evidence rules discoverable without copying the official manuals.

## Skill

- `trmnl-plugin-builder` — routes Private Plugin, Recipe, Third Party, and BYOS
  decisions; covers data paths, infrastructure boundaries, hosted-action gates,
  and verification. Use it with the official `trmnl` skill.

## What it enforces

- Default to a Private Plugin; escalate only when a Recipe, Third Party, or
  BYOS requirement actually fits.
- Prefer TRMNL's official skill, hosted MCP, `trmnlp`, live docs, and Framework
  source. Treat Context7 as a secondary cross-check.
- Keep provider and TRMNL secrets out of fields, fixtures, previews, docs, and
  generated artifacts.
- Treat hosted edits, imports, refreshes, screenshots, webhook posts, Debug
  Logs, publishing, deploys, and device checks as explicitly approval-gated.

## Attribution

See [ATTRIBUTION.md](ATTRIBUTION.md).

## License

MIT. See [LICENSE](LICENSE).
