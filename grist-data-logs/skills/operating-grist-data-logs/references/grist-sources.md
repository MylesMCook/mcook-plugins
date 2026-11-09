# Grist Sources

Checked 2026-07-10. Re-check these before changing a self-hosted instance or
depending on a newly released Grist capability.

- [REST API reference](https://support.getgrist.com/api/) documents document
  tables and columns, record upserts, OAuth-authorized record reads, and the
  parameterized read-only SQL endpoint. The SQL endpoint is API-key-only.
- [Grist MCP server](https://support.getgrist.com/mcp/) states that built-in
  self-hosted MCP is available in the Full edition, uses `/api/mcp`, and is
  disabled by default with `GRIST_MCP_ENABLED=true`.
- [Self-hosted Grist](https://support.getgrist.com/self-managed/) documents
  Community versus Full editions and persistent container requirements.
- [OAuth apps](https://support.getgrist.com/oauth-apps/) describes document
  scopes and OAuth discovery for self-hosted instances.

The REST helper deliberately uses only documented API paths. It does not claim
that Community includes the built-in MCP server.
