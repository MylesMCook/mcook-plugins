# Portable Client-Safe Architecture

## Baseline

```text
client-neutral domain and service core
        |
small MCP adapter
        |
stateless Streamable HTTP or local stdio
        |
optional MCP Apps resources
        |
optional host compatibility metadata
```

## Defaults

- Go backend for greenfield integration servers
- TypeScript only for optional UI
- remote HTTPS `/mcp` for shared servers
- stateless modern request handling
- SDK-negotiated legacy compatibility where needed
- useful tool-only results
- standard MCP Apps bridge
- capability-detected host extensions

## Portability boundaries

The core must not depend on:

- ChatGPT globals
- Claude-only metadata
- a transport session identifier
- one client's confirmation UI
- one client's resource cache behavior
- a local plugin host's rendering limitation

Put compatibility aliases in the MCP adapter. Put UI host extensions in a tiny TypeScript compatibility module.

## State

Use:

- `context.Context` for one request
- encrypted `requestState` for a modern multi-round-trip flow when required
- external storage keyed by authenticated principal for durable state
- widget state only for one rendered UI instance

Do not use MCP sessions as durable state.

## Release claim

Call a server portable only when the standard contract is proven and at least one secondary client has been tested. Otherwise name the clients that were actually validated.
