# Iframe Sandbox And CSP

MCP Apps run in a sandboxed iframe. Assume denied capabilities unless the host and declared metadata explicitly allow them.

## Baseline

- bundle JavaScript and CSS locally
- avoid CDN imports
- use host-mediated links instead of `window.open`
- use the MCP Apps bridge for host communication
- keep direct network access optional and narrow
- use `color-scheme` and host context for theme-sensitive UI
- build responsive layouts for inline and narrow surfaces

## CSP metadata

Declare exact domains:

- `connectDomains` for API requests
- `resourceDomains` for scripts, styles, images, and other assets
- `frameDomains` only for required nested frames

Prefer empty allowlists when the component can operate entirely from tool results and embedded assets.

Do not use broad wildcards to make development easier. Update the allowlist when the product requirement changes.

## Network rule

Prefer component-initiated server tool calls over direct browser calls when the server already owns authentication, authorization, rate limits, and audit logging.

Direct browser requests are valid only when:

- they materially improve the product
- the target domain is explicitly allowed
- credentials are handled safely
- the fallback path is clear
- release review expectations are understood

## Cache rule

Treat the `ui://` URI as a cache key. Publish a new URI when HTML, JavaScript, CSS, or the expected data contract changes incompatibly.
