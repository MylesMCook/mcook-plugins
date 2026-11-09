# MCP App Troubleshooting

Collect exact protocol and client evidence before changing architecture.

## No tools listed

- confirm the endpoint and connection method
- confirm modern discovery or legacy initialization succeeds for the client path being tested
- inspect `tools/list` directly
- validate schemas and metadata serialization
- refresh client metadata after tool changes

## Tool works, component does not render

Check:

- `_meta.ui.resourceUri` on the intended tool
- versioned absolute `ui://` URI
- resource registration and `resources/read`
- MIME type `text/html;profile=mcp-app`
- valid bundled HTML
- CSP and sandbox console errors
- stale client metadata or cached resource URI
- MCP Apps capability support in that client

`_meta["openai/outputTemplate"]` is a ChatGPT compatibility alias, not the portable primary field.

## Blank component

- remove CDN and remote script imports
- verify the bundle runs in a sandboxed iframe
- verify `app.connect()` runs once
- register result handlers before data is needed
- handle the initial tool result
- check DOM selectors and runtime errors
- bump the resource URI after a breaking bundle change

## Component actions fail

- call tools through the bridge, not direct internal HTTP endpoints
- verify the tool is available to component calls
- revalidate auth and permissions server-side
- add idempotency for mutation retries
- show loading and error states
- do not assume component state is authoritative

## Correct contract, one host never loads the resource

Capture:

- exact tool descriptor
- exact resource descriptor and read result
- exact tool result
- whether the host attempted a resource read
- client name, version, and connection method

If another target client and a standards-focused host render the same artifact correctly, stop refactoring the shared server. Treat the remaining issue as a host limitation or adapter task.
