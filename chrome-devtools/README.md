# Chrome DevTools

Codex plugin for browser automation, debugging, and performance analysis through the official [`ChromeDevTools/chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp) server and skills.

## What it includes

- Chrome automation and page inspection
- accessibility auditing and debugging
- Largest Contentful Paint analysis
- memory-leak diagnosis
- connection and target troubleshooting
- the optional `chrome-devtools` CLI workflow

The bundled launcher pins `chrome-devtools-mcp` to `1.5.0`, disables its optional usage statistics, and handles the different `npx` launch paths on Windows and Unix-like systems. Performance tools may still query Google's CrUX API for real-user metrics; add `--no-performance-crux` to the launcher if you do not want those requests.

## Requirements

- Node.js with `npx` available on `PATH`
- Google Chrome

The MCP server launches a dedicated Chrome profile by default. It can inspect or modify browser data available to that profile, so only use it with pages and accounts you intend Codex to access.

## Source

The skills and license are copied from the official upstream project. See [ATTRIBUTION.md](./ATTRIBUTION.md) for the pinned revision and local adaptations.
