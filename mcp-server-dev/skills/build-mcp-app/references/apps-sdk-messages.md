# MCP Apps Bridge And ChatGPT Extensions

The filename is retained for compatibility. Use the MCP Apps bridge as the portable runtime. Treat `window.openai` as an optional ChatGPT extension layer.

## Portable bridge

The component runs in a sandboxed iframe and communicates with the host through JSON-RPC over `postMessage`.

With `@modelcontextprotocol/ext-apps`:

```typescript
import { App } from "@modelcontextprotocol/ext-apps";

const app = new App({ name: "Catalog Picker", version: "1.0.0" });

app.addEventListener("toolresult", (result) => {
  render(result.structuredContent);
});

await app.connect();
```

Use the bridge for:

- initialization and host context
- tool input and tool result notifications
- component-initiated `tools/call`
- follow-up messages
- model-visible context updates
- host-mediated external links

## Shared field and ChatGPT alias mapping

| Goal | MCP Apps standard | ChatGPT compatibility or extension |
|---|---|---|
| Link a tool to UI | `_meta.ui.resourceUri` | `_meta["openai/outputTemplate"]` |
| Receive tool input | `ui/initialize` and `ui/notifications/tool-input` | `window.openai.toolInput` |
| Receive tool result | `ui/notifications/tool-result` | `window.openai.toolOutput` |
| Call a server tool | `tools/call` | `window.openai.callTool` |
| Send a follow-up | `ui/message` | `window.openai.sendFollowUpMessage` |

Use the standard column for new portable work.

When a tested host still needs the deprecated flat
`_meta["ui/resourceUri"]` key, include it beside the nested standard field as a
compatibility alias. Do not replace `_meta.ui.resourceUri` with it.

## ChatGPT-only extensions

Use `window.openai` only when ChatGPT supplies a useful capability that MCP Apps does not standardize, such as:

- file selection and upload
- host-owned modals
- checkout
- display-mode requests
- widget-state persistence

Feature-detect the exact capability through the current OpenAI typings or reference. Do not assume that every ChatGPT surface exposes every `window.openai` method.

Keep the portable path usable when the extension is absent. Do not branch on a host name.

## State rule

Widget state is presentation state for one rendered instance. It is not authoritative business state and should not be trusted for permissions, prices, mutation status, or cross-session persistence.

Store durable state on the authenticated server. Treat component calls like any other untrusted client request.
