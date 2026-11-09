---
name: build-mcp-app
description: Use when an MCP server needs optional inline UI, an interactive MCP App, a chart or dashboard, a picker, a review or confirmation surface, or a standards-first bridge between a Go MCP backend and a TypeScript component. Preserve a useful tool-only path and keep ChatGPT-specific capabilities optional.
---

# Build an MCP App

Add portable in-chat UI to a working MCP tool contract.

The default architecture is:

```text
Go MCP server
TypeScript MCP App UI
MCP Apps bridge first
Optional ChatGPT extensions
Useful tool-only fallback
```

The server does not need to be rewritten in TypeScript. MCP Apps is a wire and browser contract, not a backend-language requirement.

## Source hierarchy

Read `../../SOURCE-OF-TRUTH.md` first.

For UI work, use this order:

1. MCP Apps overview and specification
2. MCP Apps build guide and `@modelcontextprotocol/ext-apps` API
3. OpenAI Plugins UI guidance for ChatGPT behavior
4. Current documentation for any secondary client being tested

Primary pages:

- `https://modelcontextprotocol.io/extensions/apps/overview`
- `https://modelcontextprotocol.io/extensions/apps/build`
- `https://apps.extensions.modelcontextprotocol.io/`
- `https://developers.openai.com/plugins/build/chatgpt-ui`
- `https://developers.openai.com/plugins/deploy/connect-chatgpt`
- `https://developers.openai.com/plugins/reference`

Do not let a host-specific helper redefine the portable contract.

## Workflow

### 1. Inspect the existing server

Before changing code, identify:

- server language and SDK version
- transport and public endpoint
- target tool or tools
- current `content`, `structuredContent`, and `_meta` shape
- existing auth and state boundaries
- target clients and release claims

Preserve a healthy backend stack. For a Go server, add UI metadata and resources in Go.

### 2. Prove the tool-only contract

The target tool must already be useful without UI.

Require:

- clear name and description
- precise input and output schemas
- accurate annotations
- concise model-readable `content`
- stable `structuredContent`
- meaningful errors

Do not use a widget to compensate for an unclear tool contract.

### 3. Decide whether UI is justified

Add UI when the user needs to inspect, compare, edit, confirm, navigate, or manipulate structured information.

Choose the smallest useful archetype:

| Archetype | Use when |
|---|---|
| `viewer` | Read-only chart, preview, summary, or detail view |
| `picker` | Searchable or visual selection improves accuracy |
| `editor` | The user must manipulate structured state |
| `review-confirm` | A consequential action needs contextual review |
| `interactive-decoupled` | Data retrieval and rendering should be separate |

Do not port an entire website into chat. Extract the atomic conversational surface.

### 4. Choose the tool pattern

#### Simple pattern

Use one tool plus one resource when the component is small and tightly coupled to a single result.

#### Decoupled pattern

Prefer this for non-trivial apps:

- data tools return reusable `structuredContent` without UI metadata
- a render tool references the UI resource
- optional helper tools support refresh, details, or mutations

This lets the model reason over data before deciding to render. Use `references/decoupled-render-tools.md`.

### 5. Define the UI contract

Use:

- a versioned `ui://` resource URI
- MIME type `text/html;profile=mcp-app`
- `_meta.ui.resourceUri` on tools that should render the component
- `_meta.ui.csp` with exact allowlists
- useful text fallback in every tool result

Use `_meta["openai/outputTemplate"]` only as a ChatGPT compatibility alias when needed. It must not replace `_meta.ui.resourceUri`.

Add the deprecated flat `_meta["ui/resourceUri"]` key only when a tested host
still requires it. Keep the nested standard field present and authoritative.

Partition data intentionally:

| Field | Audience | Use |
|---|---|---|
| `content` | Model and user | Short narration and fallback |
| `structuredContent` | Model and UI | Stable, reusable render contract |
| `_meta` | UI or host | UI-only payloads and host metadata |

Keep `structuredContent` small enough for the model to reason over. Keep secrets and unnecessary bulk out of all three fields.

### 6. Build the TypeScript component

Default to TypeScript and Vite. Use vanilla TypeScript for a small component and React only when interaction or state complexity justifies it.

Use `@modelcontextprotocol/ext-apps` for the browser-side bridge:

- connect once
- receive tool results through `app.addEventListener("toolresult", handler)`
- call server tools through the bridge
- send follow-up messages through the bridge
- request external navigation through the host
- handle latency, retries, loading, empty, and error states

Keep the dependency graph lean. Bundle scripts and styles into one HTML resource when practical.

Use `references/widget-templates.md` and `references/go-typescript-layout.md`.

### 7. Register the app from the server

For Go:

- put the resource URI in `mcp.Tool.Meta`
- register the `mcp.Resource`
- serve the built HTML from a resource handler
- embed or read a deterministic build artifact
- keep MCP metadata assembly in the MCP adapter layer

Do not import frontend build dependencies into the Go runtime.

### 8. Add host extensions only after the standard path works

ChatGPT-specific `window.openai` APIs are optional enhancements.

Rules:

- feature-detect the exact method or field
- keep a standards-based fallback when practical
- never branch on a host or product name
- never make a ChatGPT extension the only path to a usable app
- keep business state on the server

Examples of valid ChatGPT-only enhancements include file handling, host-owned modals, checkout, display-mode requests, and widget-state persistence.

Use `references/apps-sdk-messages.md` for the mapping between portable and ChatGPT-specific APIs.

### 9. Secure the iframe and state model

Assume a sandboxed iframe and deny-by-default policy.

- use exact CSP domains
- avoid CDN imports
- avoid direct network calls unless they are necessary and declared
- use host-mediated links instead of `window.open`
- do not use browser storage as authoritative business state
- authenticate and authorize all component-initiated tool calls
- make mutations idempotent when retries are possible
- version resource URIs when the bundle contract changes

Use `references/iframe-sandbox.md`.

### 10. Validate in layers

Run:

1. frontend type check and build
2. server format, compile, and tests
3. MCP Inspector tool and resource checks
4. MCP Apps basic host or another standards-focused host
5. ChatGPT developer-mode visual test
6. a secondary real client when portability is claimed
7. mobile or narrow-layout checks for custom controls

Test both paths:

- component renders and interactions work
- component does not render, but the tool result remains useful

Use `../../CLIENT-VALIDATION-PLAYBOOK.md` and `references/chatgpt-connect-testing.md`.

## Hard rules

- Never return raw HTML from a tool handler.
- Never attach UI metadata to every tool by habit.
- Never make the component the source of truth for business data.
- Never trust prices, permissions, identifiers, or mutation state calculated only in the component.
- Never use `_meta` for data the model must reason over.
- Never claim cross-client support after testing only ChatGPT.
- Never rewrite a working Go server solely because UI examples use Node.

## Output order

When implementing or reviewing, report:

1. inspected server and tool contract
2. chosen UI archetype
3. simple or decoupled pattern
4. resource and data contract
5. files changed
6. implementation
7. validation run
8. client compatibility evidence
9. unverified host behavior or remaining release risks

For direct implementation requests, create the files and run the available checks instead of stopping at a plan.

## References

- `../../SOURCE-OF-TRUTH.md`
- `../../CLIENT-VALIDATION-PLAYBOOK.md`
- `../../CHART-PREVIEW-PATTERN.md`
- `references/apps-sdk-component-path.md`
- `references/apps-sdk-messages.md`
- `references/go-typescript-layout.md`
- `references/decoupled-render-tools.md`
- `references/widget-templates.md`
- `references/iframe-sandbox.md`
- `references/chatgpt-connect-testing.md`
- `references/claude-compatibility.md`
- `references/troubleshooting.md`
