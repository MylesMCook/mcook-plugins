# Secondary Client Compatibility

Claude web and Claude Desktop are useful secondary MCP Apps validation targets, but the release claim should be based on the exact client and version actually tested.

## Portable baseline

- standard `text/html;profile=mcp-app` resource
- versioned `ui://` URI
- `_meta.ui.resourceUri`
- MCP Apps bridge
- useful text fallback
- narrow CSP
- no host-name branching

## Validation rule

Test the same release artifact and tool contract used for ChatGPT. Capture:

- connection method
- client and version
- tool discovery result
- resource load result
- visual render
- component-initiated calls
- fallback behavior

If one client fails after the tool and resource contracts pass elsewhere, isolate the smallest host adapter or document the limitation. Do not weaken the shared core to chase an unverified quirk.

## Claims

Use precise wording:

- `MCP compatible` only after protocol tests
- `MCP Apps compatible` only after a standards-focused render test
- `Tested in ChatGPT` after real ChatGPT validation
- `Tested in Claude web` or `Claude Desktop` only after that exact surface passes

Do not generalize one passing client into universal host support.
