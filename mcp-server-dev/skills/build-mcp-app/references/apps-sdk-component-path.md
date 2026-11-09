# MCP App Component Path

The filename is retained for compatibility with the earlier plugin revision. The current architecture is MCP Apps first, with OpenAI Plugins guidance layered on for ChatGPT.

## Canonical sources

### Portable standard

- [MCP Apps overview](https://modelcontextprotocol.io/extensions/apps/overview)
- [Build an MCP App](https://modelcontextprotocol.io/extensions/apps/build)
- [MCP Apps API](https://apps.extensions.modelcontextprotocol.io/)
- [MCP Apps source and examples](https://github.com/modelcontextprotocol/ext-apps)

### ChatGPT integration

- [Add UI to your MCP server](https://developers.openai.com/plugins/build/chatgpt-ui)
- [UI guidelines](https://developers.openai.com/plugins/guides/ui-guidelines)
- [Connect and test](https://developers.openai.com/plugins/deploy/connect-chatgpt)
- [Plugin UI reference](https://developers.openai.com/plugins/reference)

## Order

1. Confirm the tool works without UI.
2. Decide what the user must see or manipulate.
3. Choose viewer, picker, editor, review-confirm, or interactive-decoupled.
4. Define `content`, `structuredContent`, and `_meta` boundaries.
5. Assign a versioned `ui://` URI.
6. Register the tool metadata and HTML resource.
7. Build the component on the MCP Apps bridge.
8. Add ChatGPT extensions only when the standard does not cover the capability.
9. Validate the fallback and visual paths independently.
10. Test another client before claiming portability.

## Practical checks

- The component improves the conversational workflow.
- The smallest useful presentation is used.
- The tool remains useful when no component renders.
- The resource uses `text/html;profile=mcp-app`.
- `_meta.ui.resourceUri` is the primary pointer.
- The resource URI changes when the bundle contract changes.
- CSP allowlists match actual network behavior.
- Durable state and authorization remain server-side.
- ChatGPT-only APIs are capability-detected.
