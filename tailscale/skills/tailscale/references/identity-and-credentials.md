# Identity, credentials, and tsidp

> Credential types and API scopes have changed more than once. Fetch the matching
> page for current scope names, expiries, and console paths before writing
> automation. Never paste real keys or secrets into chat or logs.

## Choose the credential

| Goal | Use |
|------|-----|
| Join a server, container, or CI runner to the tailnet | **Auth key** (usually tagged, often ephemeral), or a trust credential that mints keys |
| Long-running automation against the API with least privilege | **Trust credential**: an **OAuth client** (client ID + secret) |
| CI or cloud workloads without a stored secret | **Trust credential**: **workload identity federation** (exchange the platform's OIDC token) |
| An internal tool acting as the signed-in human, with their identity in audit logs | **OAuth app** (authorization code flow, same tailnet only) |
| Quick personal scripting | API access token (full access, expires; avoid for shared automation) |

OAuth **clients** create tag-owned resources under a service identity. OAuth
**apps** act on behalf of an individual user. Do not confuse the two.

## tsidp

`tsidp` is an experimental, open-source OIDC/OAuth server that runs on the
tailnet and identifies users by their Tailscale connection, so apps that support
OIDC (Grafana, Proxmox, MCP servers) get "Log in using Tailscale" with no extra
password. It needs MagicDNS and HTTPS enabled and policy-file grants for its
capabilities. Expect breaking changes; fetch the current config page.

## Where to find current information

| Need | Page |
|------|------|
| All key and secret types | https://tailscale.com/docs/reference/key-secret-management |
| Auth keys | https://tailscale.com/docs/features/access-control/auth-keys |
| Trust credentials and scopes | https://tailscale.com/docs/reference/trust-credentials |
| OAuth clients | https://tailscale.com/docs/features/oauth-clients |
| Workload identity federation | https://tailscale.com/docs/features/workload-identity-federation |
| OAuth apps | https://tailscale.com/docs/features/oauth-apps |
| OAuth hub | https://tailscale.com/docs/oauth |
| tsidp | https://tailscale.com/docs/features/tsidp |
| tsidp configuration | https://tailscale.com/docs/reference/tsidp-configuration |
| Key prefixes (identify a leaked key) | https://tailscale.com/docs/reference/key-prefixes |
