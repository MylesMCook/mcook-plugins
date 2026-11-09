# Myles agent plugins

Plugin marketplace for Codex, Claude, Claude Code, and Cursor.

Licenses and attribution vary by package. See each package's license and
[publication licensing review](docs/publication-licensing.md); this repository
does not grant a blanket license over all included material.

## Codex

Add the marketplace, browse plugins, and install one:

```sh
codex plugin marketplace add https://github.com/MylesMCook/mcook-plugins.git --ref main
codex plugin list --marketplace mcook-plugins-local --available
codex plugin add thermos@mcook-plugins-local
```

Replace `thermos` with the plugin you want. Start a new task after installing.

[Cici](cici/README.md) packages the three direct Claude Code CLI skills as
`cici@mcook-plugins-local`: questions, read-only review, and rescue planning.
[Skills for Golang](https://github.com/samber/cc-skills-golang) is available as
`cc-skills-golang@mcook-plugins-local`. This external Codex-native package tracks
upstream `main`; refresh and reinstall to fetch updates. See the
[connection, owner-approved exception, and verification](docs/external-golang-plugin.md).
To update, finish tasks using the plugin, then run:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add thermos@mcook-plugins-local
```

Repeat `plugin add` for each plugin you want to update, then start a new task.

## Claude and Claude Code

On claude.ai, open **Customize → Plugins → Add → Add marketplace**, choose
**Add from a repository**, and enter `MylesMCook/mcook-plugins`.

The Claude catalog includes explicit Claude manifests. Fabric's Windows
executable package is available in Codex and Cursor; it is excluded from Claude
because cloud sync rejects top-level `bin/` directories. Local MCP servers
(such as Explainer) run in Cowork and Claude Code, not in web chat.

For Claude Code:

```sh
claude plugin marketplace add MylesMCook/mcook-plugins
claude plugin install thermos@mcook-plugins
```

To update:

```sh
claude plugin marketplace update mcook-plugins
claude plugin update thermos@mcook-plugins
```

## Cursor

In **Dashboard → Plugins → Team Marketplaces**, choose **Add Marketplace →
Import from Repo**. Enter `https://github.com/MylesMCook/mcook-plugins`, select
`main`, and grant repository access if prompted. Enable Auto Refresh for updates.

See each plugin's README for setup and usage. Available plugins vary by client:
[Codex](.agents/plugins/marketplace.json),
[Claude Code](.claude-plugin/marketplace.json),
[Cursor](.cursor-plugin/marketplace.json).
