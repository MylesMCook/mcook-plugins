# Native development feedback

The feedback tools are a stdio MCP server, `wails-feedback/mcp.mjs`, usable from
any MCP client. To connect Codex once from the repository root:

```sh
pnpm --dir app feedback:connect
```

Open a new agent session once after connecting. Every later development run needs only:

```sh
pnpm --dir app dev:feedback
```

Keep that terminal open. Add comments with the Agentation toolbar and ask your
agent to read and act on pending feedback, verify changes, and resolve each
comment only after verification. The same connection follows Burf restarts
and new private ports. It also loads its tools when Burf is closed and explains
how to start feedback when a tool is used while offline.

The connection uses the existing pinned Agentation MCP tools through stdio.
It reads the current private run for each request. It starts no app or background
service, binds no extra listener, and never retries an interrupted write.
After an interrupted request, check the comment's status before repeating it.

Disconnect before undoing native-feedback setup:

```sh
pnpm --dir app feedback:disconnect
```

Disconnect is safe to rerun and preserves private comments. Connection setup
refuses to overwrite a different server with the same name. The registration is
local to the machine running the agent. Feedback remains development-only and
excluded from production bundles. `--inspect` is optional for native inspection.

These root commands show Burf's split pnpm layout. In other generated apps,
run the same script names with the existing package manager from the detected
frontend folder. Other MCP clients (Claude Code, Factory Droid, Cursor, and others) can register
`node wails-feedback/mcp.mjs` from that folder in their own MCP configuration.
The connection helper uses the Codex CLI specifically; the stdio launcher and
feedback tools work with any MCP client.
