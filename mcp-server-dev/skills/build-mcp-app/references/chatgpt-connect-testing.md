# ChatGPT Connect And Testing

Use this after the MCP server and optional UI resources pass local checks.

## Prepare the endpoint

Use either:

- a public HTTPS Streamable HTTP endpoint, usually ending in `/mcp`
- Secure MCP Tunnel for private developer-mode testing
- another temporary HTTPS tunnel for local development

A temporary tunnel is not a production release endpoint.

## Connect in ChatGPT

1. Open ChatGPT Settings.
2. Select **Security and login**.
3. Enable **Developer mode**.
4. Open **ChatGPT Plugins**.
5. Add a connection.
6. Enter the public `/mcp` URL or select the configured Secure MCP Tunnel.
7. Review the discovered tools and metadata.

Product labels may change. Recheck the current OpenAI Plugins connect-and-test page when these steps no longer match the UI.

## Validation order

1. MCP Inspector
2. MCP Apps basic host or another standards-focused host
3. ChatGPT developer-mode tool selection
4. ChatGPT visual render and component interaction
5. tool-only fallback in a non-rendering path
6. a secondary real client when portability is claimed
7. narrow and mobile layout checks

## Evaluation set

Include:

- direct prompts that should select one tool
- indirect prompts expressing the same goal
- follow-ups that reuse returned identifiers
- empty and large results
- invalid input and permission failures
- write actions that require confirmation
- unsupported requests that should not call a tool
- component-initiated calls and retries
- the same workflow without UI

Record selected tool, arguments, result, visible component state, errors, and confirmation behavior.

## Refresh after changes

After changing tools, schemas, annotations, auth, resource metadata, or UI:

1. deploy or restart the server
2. bump the `ui://` URI when the bundle contract changed
3. refresh the connection in ChatGPT Plugins
4. confirm the discovered metadata changed
5. start a new conversation
6. rerun the affected evaluation cases

Do not diagnose stale metadata by repeatedly changing a correct server contract.
