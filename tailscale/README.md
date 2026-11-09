# Tailscale

One skill for explaining, configuring, and troubleshooting Tailscale, adapted
from [Tailscale's upstream skill](https://github.com/tailscale/tailscale-skill).
Its 17 focused references cover networking, access controls, containers,
enterprise administration, session recording, Aperture, Border0, and tsnet.

Install from Myles Codex Plugins:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add tailscale@mcook-plugins-local
```

Start a new task, then ask:

- `Use $tailscale to diagnose my tailnet connectivity.`
- `Use $tailscale to plan a subnet router with a rollback path.`
- `Use $tailscale to explain Serve versus Funnel for this app.`

This package contains guidance, not a Tailscale client, MCP server, hook, or
background service. Installation does not change your network or authenticate
devices. The skill uses available documentation tools and checks local CLI help
before applying authorized changes.

Upstream labels the skill an unsupported public alpha. Its bundled examples
are a snapshot; current official documentation and installed-version checks
govern concrete configuration. See [ATTRIBUTION.md](ATTRIBUTION.md) for the
source commit and adaptation details, and [LICENSE](LICENSE) for BSD-3-Clause.
