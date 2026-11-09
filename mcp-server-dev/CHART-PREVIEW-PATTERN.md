# Chart Preview Pattern

Use this for preview-style MCP Apps that help author or review Vega, Vega-Lite, Deneb, and Power BI custom visuals.

## Default shape

```text
Go preview server
TypeScript renderer
One data or preview tool
One versioned ui:// resource
Useful text fallback
```

Keep the surface tight:

- one read-only `preview_*` tool for a simple workflow
- a data tool plus render tool when model inspection must happen before rendering
- normalized preview data in `structuredContent`
- minimal UI-only data in `_meta`
- client-side rendering inside the widget
- an external editor link only as a fallback

## Tool contract

Return:

- a short useful summary in `content`
- grammar, normalized spec, renderability, warnings, and fallback URL in `structuredContent`
- sensitive or bulky UI-only data in `_meta` only when necessary

The tool must remain useful without custom UI.

## Widget contract

The widget must:

- use `text/html;profile=mcp-app`
- use a versioned `ui://...` URI
- be referenced through `_meta.ui.resourceUri`
- render from `structuredContent`
- use the MCP Apps bridge for tool calls and messages
- capability-detect optional ChatGPT extensions
- declare the narrowest practical CSP
- work at narrow widths and without hover-only controls

Do not return raw HTML from a tool handler.

## Validation

1. Unit-test normalization and warnings.
2. Prove modern and claimed legacy MCP paths.
3. Inspect the tool and resource contract.
4. Render in ChatGPT.
5. Render in another compatible client when portability matters.
6. Compare the rendered result against a known-good editor for representative specs.

A convenience host showing only text is not proof that the server is broken when the standard contract and target clients pass.
