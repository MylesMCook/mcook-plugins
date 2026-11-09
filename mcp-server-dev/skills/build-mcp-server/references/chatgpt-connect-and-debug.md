# ChatGPT Connect And Debug

Use this after the remote server passes local build and protocol checks.

## Connect

1. Expose the server through public HTTPS or Secure MCP Tunnel for development.
2. Keep the MCP endpoint at `/mcp`.
3. In ChatGPT, open Settings.
4. Select Security and login.
5. Enable Developer mode.
6. Open ChatGPT Plugins.
7. Add the MCP connection and review discovered tools.
8. Start a new conversation with the connection enabled.

Developer-mode availability can depend on account and workspace policy.

## Refresh

After changing tools, schemas, annotations, auth, or UI resources:

1. deploy or restart the server
2. open the connection in ChatGPT Plugins
3. select Refresh
4. confirm the discovered metadata changed
5. start a new conversation
6. rerun affected evaluation prompts

Published metadata uses a reviewed snapshot. A developer-mode refresh is not a published update.

## Debug order

1. Clean build and tests
2. Modern protocol request
3. Claimed legacy protocol request
4. Exact tool and resource contract
5. Auth discovery and authorization
6. ChatGPT connection discovery
7. Tool selection in a real conversation
8. Optional UI resource fetch and render
9. Browser console and server logs
10. Secondary client when portability matters

## Common failures

### No tools

- wrong URL or missing `/mcp`
- transport rejected
- protocol version mismatch
- auth middleware blocked discovery
- schema or handler registration failed

### Tool runs but UI does not render

- missing `_meta.ui.resourceUri`
- URI does not match the registered resource
- wrong MIME type
- stale unversioned resource URI
- CSP blocks the bundle or network request
- client lacks MCP Apps support

### Metadata looks stale

Refresh the connection and start a new conversation. Bump the `ui://` URI when the HTML contract changes.

### Standard contract passes but one host fails

Preserve the working core. Isolate the failure as a host compatibility issue and add only the smallest verified adapter.
