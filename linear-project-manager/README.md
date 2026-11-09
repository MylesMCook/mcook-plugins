# Linear Project Manager

Keep meaningful development work in Linear without managing a ticket for every
agent step. One skill reuses outcome issues across machines, records verification,
and leaves incomplete work visibly unfinished.

## What runs

- A portable Agent Plugins 1.0.0 package containing one Agent Skill and the official Linear
  Streamable HTTP MCP declaration.

There are no automatic hooks or background processes. Invoke the skill for
tracked work, or use an approved repository instruction to apply it. A crash can
leave Linear stale until the next invocation.

## Setup on each machine

1. Install `linear-project-manager@mcook-plugins-local` after it is published.
2. Connect/authenticate the declared official Linear MCP through the client's
   normal OAuth flow. If Linear is already connected, reuse that connection;
   avoid configuring another global server. No API key is bundled.
3. Start a new task and ask: `Use $linear-project-manager to map this repo to Linear.`
   Confirm the team/project and automatic issue-maintenance scope once per repo.
   The approved mapping lives in that repo's existing AGENTS.md and travels with Git.

Existing repository instructions, including any tasks.md requirement, remain in effect.

## Boundaries

Questions and trivial edits create no issue unless requested. Meaningful bugs and
features get one outcome issue. Done requires the agreed evidence and any required
review or delivery. Linear outages never stop development; unsynced work is reported.
Project creation, deletion, assignment, and changes outside the mapped repo are not
part of automatic issue maintenance. Authentication is per machine/client and does
not travel with the mapping. Concurrent create deduplication is best effort.

## Verification

Run `python3 -m unittest discover -s linear-project-manager/tests` from the repository
root with Python 3.9+ and Codex available. The fresh-home installation test checks
that Codex loads one skill and the Linear MCP declaration with zero plugin hooks.
See [behavioral review](tests/behavioral-review.md) for workflow cases and
verification limits. The MCP connection uses current/default remote protocol negotiation;
no specific protocol revision or authenticated handshake is claimed.

Sources checked 2026-09-22: [Linear MCP](https://linear.app/docs/mcp) and
[plugin packaging](https://developers.openai.com/plugins/build/plugins).

## Packaging compatibility

Root `plugin.json`, fixed `skills/`, and root `mcp.json` follow
[Agent Plugins 1.0.0](https://agent-plugins.org/specification). The portable MCP
declaration uses `streamable-http`. Codex interface metadata lives under
`extensions.com.openai`.

The matching `.codex-plugin/plugin.json` and `.mcp.json` files retain compatibility
with native Codex installations. Their identity, version, Linear endpoint, and
transport mapping are checked against the portable core. The historical
native-only exception concerned hooks removed in 0.1.1; it is no longer needed.

Those legacy files belong to a separate Codex compatibility format outside the
portable core. Conformance claims cover the portable core; strict conformance of
the complete legacy distribution is not claimed. The portable-only check removes
both legacy files and still discovers the skill and Linear connection.

Installation and discovery are tested on Codex, both with the compatibility
files and with only the portable core. Other clients' runtime behavior and
authenticated Linear operations are not established by these checks. This
release preserves existing catalog membership.

Run the native installation regression with:

```sh
python3 -m unittest discover -s linear-project-manager/tests -p test_native_ingestion.py
```

It installs only into a temporary Codex home, checks byte parity, skill and MCP
discovery, and the absence of plugin hooks. It does not authenticate Linear. Set
`CODEX_TEST_BINARY` to test another already-installed Codex executable.
