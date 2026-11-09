# Lawful

Lawful packages three separate law-based skills. Each one has a narrow job.

| Skill | Use it for |
| --- | --- |
| `laws-of-software-los` | Architecture, system boundaries, migrations, incidents, and technical tradeoffs |
| `laws-of-taste` | Visual hierarchy, typography, color, spacing, interaction feel, and design polish |
| `laws-of-ux-lou` | Focused UX critique using the two to four laws that matter most to the user flow |

## Use in Codex

```text
$lawful:laws-of-software-los Review this migration plan. Recommend the smallest
reversible design and name the validation and rollback path.
```

```text
$lawful:laws-of-taste Critique this dashboard and give me the strongest few
visual changes.
```

```text
$lawful:laws-of-ux-lou Review this checkout flow with the most relevant Laws of
UX. Keep the critique specific to what is on screen.
```

Codex can activate each skill when a request fits its description. Laws of
Software applies to substantive architecture decisions, not ordinary code
changes. The three skills stay separate so each task gets the relevant lens
without loading the others.

## Behavior

- This plugin has no MCP server, app, account, authentication, or background process.
- No hooks are bundled or installed.
- Each bundled skill keeps its relevant references, scripts, license, and notice files.

## Provenance

The three skills come from `MylesMCook/mcook-skills` at commit
`a0230d441e3c30fef8516b3300951ffa23e1279e`. See
[ATTRIBUTION.md](ATTRIBUTION.md) for source links and license details.

## License

Lawful's package files use the MIT License. Each bundled skill retains its own
MIT license and any required notice.
