# OpenAI Plugin Deploy Track

This filename is retained for compatibility. The current product documentation is OpenAI Plugins documentation.

## Canonical docs

- [Build an MCP server](https://developers.openai.com/plugins/build/mcp-server)
- [Connect and test](https://developers.openai.com/plugins/deploy/connect-chatgpt)
- [Troubleshooting](https://developers.openai.com/plugins/deploy/troubleshooting)
- [MCP server review requirements](https://developers.openai.com/plugins/deploy/app-review)
- [Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [Submit and publish](https://developers.openai.com/plugins/deploy/submission)

## Order

1. Prove build and protocol truth locally.
2. Expose a stable Streamable HTTP endpoint at `/mcp`.
3. Use MCP Inspector or an equivalent protocol test client.
4. Enable ChatGPT developer mode.
5. Register the MCP server through ChatGPT Plugins.
6. Review discovered tools and metadata.
7. Run the versioned evaluation prompt set.
8. Refresh the connection after metadata changes.
9. Test optional UI separately from the model-readable result.
10. Package the complete plugin only after the server contract is stable.
11. Re-run security, privacy, auth, and review checks before public submission.

Secure MCP Tunnel and temporary development tunnels are development tools, not substitutes for the stable public HTTPS endpoint required by public submission.

Keep protocol truth, server contract truth, and ChatGPT product truth separate.
