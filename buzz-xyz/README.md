# Buzz.xyz

`buzz-xyz` is a skills-only plugin for operating a Buzz relay through the
installed `buzz` command-line interface.

## What it covers

- Messages, mentions, channels, DMs, users, feeds, reactions, and forum posts.
- Owner-reviewed agent drafts and updates.
- Workflows, canvas, social data, file uploads, and agent memory.
- Buzz-hosted Git repositories and repository protection rules.
- Buzz-specific output contracts, exit codes, pagination, conflict handling,
  and known relay limitations.

The plugin does not bundle the Buzz CLI, an MCP server, hooks, a UI, or relay
credentials. The `buzz` executable must already be available on `PATH`, and
the runtime must provide `BUZZ_PRIVATE_KEY`. Owner-reviewed agent drafts also
need `BUZZ_AUTH_TAG`. The skill never reads or prints those values.

## Use in Codex

Invoke the skill directly:

```text
$buzz-xyz:buzz-cli Summarize recent activity in my Buzz channels.
```

The skill can also be selected implicitly when a task specifically asks to
inspect or operate Buzz.

## Package shape

Version `0.2.1` contains one portable Agent Skill plus the OpenAI compatibility
manifest. The external Buzz CLI remains the runtime boundary.

## Install or refresh

After this plugin is published to `mcook-plugins-local`, close active tasks
using it and run:

```sh
codex plugin marketplace upgrade mcook-plugins-local
codex plugin add buzz-xyz@mcook-plugins-local
codex plugin list | rg 'buzz-xyz@mcook-plugins-local'
```

Start a new Codex task after installation so it loads the skill metadata.

## Source and license

The skill adapts Block's Buzz managed-agent skill. See
[ATTRIBUTION.md](ATTRIBUTION.md).

Licensed under Apache-2.0. See [LICENSE](LICENSE).
