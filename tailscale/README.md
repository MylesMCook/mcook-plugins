# Tailscale

One skill for explaining, configuring, and troubleshooting Tailscale, adapted
from [Tailscale's upstream skill](https://github.com/tailscale/tailscale-skill).
It is docs-first: the agent checks local `tailscale help` and reads the live
official page (as Markdown) before relying on bundled examples. References cover
networking, access control, Services and route selection, credentials and tsidp,
containers, enterprise administration, session recording, Aperture, Tailscale
PAM (formerly Border0), and tsnet, plus a map of the official docs.

Install from Myles Codex Plugins:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add tailscale@mcook-plugins-local
```

Claude Code and Factory Droid install it from the `mcook-plugins` marketplace
(for example `claude plugin install tailscale@mcook-plugins`).

Start a new task, then invoke the skill by name (for example `$tailscale` or
`/tailscale`):

- `Use $tailscale to diagnose my tailnet connectivity.`
- `Use $tailscale to plan a subnet router with a rollback path.`
- `Use $tailscale to explain Serve versus Funnel for this app.`

This package contains guidance, not a Tailscale client, MCP server, hook, or
background service. Installation does not change your network or authenticate
devices.

## Optional: Tailscale's docs search server

Tailscale runs a documentation search MCP server at
`https://tailscale.mcp.kapa.ai/` (hosted by Kapa, browser sign-in on first use).
The skill uses it when your agent has it, but does not bundle it. Add it in your
agent's MCP settings if you want search on top of page fetches.

## Staying current

`scripts/check_freshness.py` compares the skill with Tailscale's live docs: every
cited docs URL must still resolve without a redirect or deprecation notice, every
section and feature page in `https://tailscale.com/docs/llms.txt` must appear in
`references/docs-map.md`, and the upstream skill must still match the pinned
commit. The `Tailscale docs freshness` workflow runs it weekly and on changes;
a failed run lists what to update.

Upstream labels the skill an unsupported public alpha. See
[ATTRIBUTION.md](ATTRIBUTION.md) for the source commit and changes, and
[LICENSE](LICENSE) for BSD-3-Clause.
