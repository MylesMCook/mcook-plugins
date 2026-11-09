# Portable Release Checklist

## Repository

- [ ] Clean checkout builds without undocumented local state
- [ ] Dependency versions are pinned
- [ ] Generated files are reproducible or clearly committed
- [ ] Domain code is independent of MCP SDK types
- [ ] Secrets and private endpoints are absent from source and examples
- [ ] License and third-party notices are correct
- [ ] Changelog identifies contract changes

## Protocol

- [ ] Remote server uses stable `/mcp`
- [ ] Modern `2026-07-28` path is explicitly tested
- [ ] `server/discover` is tested when used by the client or validation suite
- [ ] Every legacy version claimed is tested
- [ ] No business state depends on MCP session IDs
- [ ] Tool and resource lists are deterministic
- [ ] Cache metadata and invalidation behavior are reviewed
- [ ] `resultType` and multi-round-trip behavior are tested when used
- [ ] Cancellation and request deadlines are honored

## Tool contract

- [ ] One job per tool
- [ ] Accurate names, titles, and `Use this when...` descriptions
- [ ] Bounded schemas and explicit output schemas
- [ ] Correct read-only, destructive, idempotent, and open-world annotations
- [ ] Useful text content
- [ ] Reusable structured content
- [ ] Errors are model-readable without leaking internals
- [ ] Retry behavior is documented and tested

## Security

- [ ] Authentication discovery works
- [ ] Issuer, audience, expiry, and scopes are validated
- [ ] Authorization is checked per resource or action
- [ ] Incoming bearer tokens are not passed through upstream
- [ ] User state is keyed by authenticated principal
- [ ] Rate limits and request-size limits exist
- [ ] SSRF, path traversal, command execution, and webhook boundaries are tested where relevant
- [ ] Logs omit secrets and unnecessary personal data

## MCP Apps

- [ ] Tool-only behavior remains useful
- [ ] Standard `_meta.ui.resourceUri` is primary
- [ ] Resource MIME type is `text/html;profile=mcp-app`
- [ ] Resource URI is versioned
- [ ] CSP is minimal
- [ ] MCP Apps bridge is primary
- [ ] ChatGPT extensions are capability-detected
- [ ] Narrow and mobile layouts work
- [ ] Durable business data remains server-owned

## Operations

- [ ] Health and metrics endpoints are separate from `/mcp`
- [ ] Structured logs identify method and tool without logging sensitive arguments
- [ ] Timeouts and upstream retries are bounded
- [ ] Idempotency strategy exists for writes
- [ ] Deployment supports horizontal scaling without sticky sessions
- [ ] Rollback procedure is documented
- [ ] Artifact checksums or image digests are published

## Client evidence

- [ ] Protocol test client or Inspector
- [ ] ChatGPT developer-mode evaluation
- [ ] Secondary client when broad portability is advertised
- [ ] Negative and out-of-scope prompts
- [ ] Authentication and confirmation behavior
- [ ] Known host-specific limitations documented separately
