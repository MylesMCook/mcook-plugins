# Firecrawl endpoints

Read the MCP endpoint from the user's local client configuration. This package
contains no production or staging address. Keep deployment-specific hostnames,
paths and credentials outside source control.

The example local API is `http://127.0.0.1:3002`; use the deployment's actual
address and run CLI operations only on a machine allowed to reach it.

## Read-only checks

Check the configured server and its authentication without restarting services.
For a remote MCP endpoint, expect the deployment's documented authentication
challenge when unauthenticated. A reachable edge and challenge do not prove the
current task is logged in; verify `search` and `fetch` before claiming usability.

Use the deployment's operator documentation for service status commands. Do not
start, stop or restart services merely to satisfy a plugin check. Ask before
changing a persistent service.
