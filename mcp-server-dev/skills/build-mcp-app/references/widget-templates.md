# Widget Templates

Use these as compact UI starting points. The server may be Go, Rust, TypeScript, Python, or another compliant implementation. These templates cover only the browser component.

## Base HTML

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MCP App</title>
    <style>
      :root { color-scheme: light dark; font-family: system-ui, sans-serif; }
      body { margin: 0; padding: 12px; }
      button { font: inherit; }
    </style>
  </head>
  <body>
    <main id="root" aria-live="polite">Loading...</main>
    <script type="module" src="/src/app.ts"></script>
  </body>
</html>
```

Bundle the final HTML and scripts together when practical. Serve it as `text/html;profile=mcp-app` from a versioned `ui://` resource.

## Viewer

Use for charts, previews, summaries, and read-only detail.

```typescript
import { App } from "@modelcontextprotocol/ext-apps";

const app = new App({ name: "Result Viewer", version: "1.0.0" });
const root = document.querySelector<HTMLElement>("#root")!;

app.addEventListener("toolresult", (result) => {
  const data = result.structuredContent;
  root.textContent = data ? JSON.stringify(data, null, 2) : "No data returned.";
});

await app.connect();
```

Replace the JSON renderer with the smallest domain-specific view that earns its place in chat.

## Picker

Use for a searchable or visual selection. Send a follow-up through the bridge rather than mutating server state locally.

```typescript
import { App } from "@modelcontextprotocol/ext-apps";

type PickerItem = { id: string; label: string };

const app = new App({ name: "Result Picker", version: "1.0.0" });
const root = document.querySelector<HTMLElement>("#root")!;

app.addEventListener("toolresult", (result) => {
  const data = result.structuredContent as { items?: PickerItem[] } | undefined;
  const buttons = (data?.items ?? []).map((item) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = item.label;
    button.addEventListener("click", () => {
      void app.sendMessage({
        role: "user",
        content: [{ type: "text", text: `Select item ${item.id}.` }],
      });
    });
    return button;
  });
  root.replaceChildren(...buttons);
});

await app.connect();
```

Use a server tool call instead when the click itself performs an authenticated action:

```typescript
async function selectItem(item: PickerItem) {
  return app.callServerTool({
    name: "select_item",
    arguments: { id: item.id, idempotencyKey: crypto.randomUUID() },
  });
}
```

## Review and confirm

Use for contextual review before a consequential mutation.

- Render authoritative data returned by the server.
- Label the exact effect.
- Keep cancel easy.
- Call a dedicated mutation tool only after explicit user action.
- Make the mutation idempotent and re-authorize it server-side.

## Progress

For long-running work, prefer the MCP Tasks extension when the server needs durable asynchronous execution. Use component progress only as a view over authoritative server state.

## Required states

Every component should deliberately handle:

- loading
- empty result
- recoverable error
- permission or authentication error
- stale or conflicting state
- successful action
- host capability unavailable

The tool's text fallback must remain meaningful in all cases.
