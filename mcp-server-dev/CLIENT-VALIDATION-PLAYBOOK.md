# Client Validation Playbook

Use this after the shared MCP core is implemented and before release.

## Four truths

Keep these separate.

1. **Build truth**: the repository formats, compiles, tests, and produces the intended artifacts.
2. **Protocol truth**: the server speaks every protocol version and transport it claims.
3. **Contract truth**: tools, resources, schemas, annotations, results, auth, and UI metadata are correct.
4. **Client truth**: the actual target clients select tools, render optional UI, and handle errors correctly.

Passing one layer does not prove the others.

## Protocol matrix

Test both rows when broad compatibility is a release goal.

| Path | Required evidence |
|---|---|
| MCP `2026-07-28` | Request includes `MCP-Protocol-Version: 2026-07-28`; `server/discover` works when used; direct list and call requests work without a session; responses include the expected `resultType`; repeated requests can land on different instances |
| Legacy supported version | The SDK-negotiated `initialize` flow, advertised capabilities, tool list, resource access, and calls work through the same endpoint |

Do not describe a server as `2026-07-28` compatible because it starts or because a legacy Inspector connection succeeds.

## Contract checks

Capture and review:

- tool list in deterministic order
- tool names, titles, descriptions, schemas, output schemas, and annotations
- representative valid and invalid calls
- model-readable `content`
- reusable `structuredContent`
- UI-only `_meta`
- resource list and resource reads
- `text/html;profile=mcp-app` for UI resources
- versioned `ui://` resource URIs
- exact CSP and permissions
- authentication discovery and authorization failures
- retry behavior for idempotent and non-idempotent tools

## Client ladder

Use this order unless the release names a different primary client.

1. Static checks, unit tests, and integration tests
2. MCP Inspector or a protocol test client
3. ChatGPT developer mode
4. One secondary compatible client when portability is claimed
5. Mobile or narrow layout testing for custom UI
6. Public deployment and submission checks when relevant

Codex is the authoring surface. Do not treat Codex convenience rendering as the sole runtime verdict.

## Prompt evaluation set

Maintain a small versioned set containing:

- direct requests that should select one tool
- indirect requests expressing the same goal
- follow-ups that reuse returned identifiers
- empty, missing, and boundary inputs
- write actions requiring confirmation or authorization
- unsupported requests that should not call a tool
- attempts to access another user's data
- retry and duplicate-delivery cases

Record selected tool, arguments, result, error, confirmation, and UI outcome.

## MCP App checks

Verify:

- the tool remains useful when UI is unavailable
- only render tools attach `_meta.ui.resourceUri` in a decoupled design
- the host fetches the exact resource URI
- the UI renders from `structuredContent`
- component-initiated calls go through the MCP Apps bridge
- ChatGPT-only APIs are capability-detected
- state survives the interactions it claims to support
- durable business data remains server-owned
- CSP failures, stale resource URIs, and console errors are absent

## Failure triage

Before changing architecture, collect:

- protocol version and HTTP headers
- exact method and tool name
- exact tool descriptor
- exact resource descriptor and contents
- exact call result
- server logs for that request
- whether the client attempted the resource fetch
- client-visible error and console output

If the standard contract passes in protocol tests and another real client, isolate a remaining failure as a client compatibility issue. Do not weaken the shared contract to satisfy a non-target convenience host.

## Release gate

A portable release is ready only when:

- build and tests pass from a clean checkout
- the modern path is proven
- every claimed legacy path is proven
- security and auth boundaries are tested
- ChatGPT behavior is tested
- another client is tested when broad compatibility is advertised
- artifact versions, checksums, and deployment instructions are documented
- known host-specific limitations are explicit
