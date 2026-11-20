# Tailscale documentation map

Reviewed against live docs: 2026-11-20.

Use this file to find the right official page, then read the live page. It is a
map, not a source of facts.

## Retrieval order

1. **Local truth for operations.** On a device, check `tailscale version` and
   `tailscale help <subcommand>` (or `--help`) before suggesting flags. The
   installed client wins over docs for flag syntax on that machine.
2. **Live page as Markdown.** Append `.md` to any `https://tailscale.com/docs/...`
   URL to get clean Markdown, for example
   `https://tailscale.com/docs/features/exit-nodes.md`. Read the
   "Last validated" date and any release-stage note (alpha, beta, GA) at the top.
3. **Discover pages.** When no reference lists a page, read the curated index at
   `https://tailscale.com/docs/llms.txt` and pick the page from there.
4. **Search.** If the environment has Tailscale's documentation search MCP server
   (`https://tailscale.mcp.kapa.ai/`, optional, the user adds it) or a general
   web search tool, use it for questions the index doesn't resolve. Prefer
   `tailscale.com/docs` results over blogs and forums.
5. **Recent changes.** For "did this change", version, or security questions, read
   `https://tailscale.com/changelog` and `https://tailscale.com/security-bulletins`.

Redirects and deprecation notices mean the reference here is stale: follow the
new page, tell the user what moved, and prefer the new name.

## Section roots

| Section | Root | Main reference |
|---|---|---|
| Install Tailscale on any device | https://tailscale.com/docs/install | `installation.md` |
| Use cases | https://tailscale.com/docs/use-cases | SKILL.md task router |
| Solutions | https://tailscale.com/docs/solutions | SKILL.md task router |
| Features | https://tailscale.com/docs/features | see below |
| Aperture | https://tailscale.com/docs/aperture | `aperture.md` |
| Tailscale PAM | https://tailscale.com/docs/privileged-access-management | `pam.md` |
| Tailscale Kubernetes Operator | https://tailscale.com/docs/kubernetes-operator | `containers.md` |
| How-to Guides | https://tailscale.com/docs/how-to | per topic |
| Hubs | https://tailscale.com/docs/automations | per topic |
| Integrations | https://tailscale.com/docs/integrations | per topic |
| Manage your organization | https://tailscale.com/docs/account | `device-management.md` |
| Technical overviews | https://tailscale.com/docs/concepts | `connectivity.md` |
| Technical reference | https://tailscale.com/docs/reference | `cli.md`, `api.md` |

## Feature pages

| Page | Reference |
|---|---|
| https://tailscale.com/docs/features/access-control | `access-control.md` |
| https://tailscale.com/docs/features/app-connectors | `services-and-routing.md` |
| https://tailscale.com/docs/features/declarative-node-sharing | `access-control.md` |
| https://tailscale.com/docs/features/device-posture | `device-management.md` |
| https://tailscale.com/docs/features/ephemeral-nodes | `enterprise.md` |
| https://tailscale.com/docs/features/exit-nodes | `exit-nodes.md` |
| https://tailscale.com/docs/features/firewall-mode | `subnet-routers.md` |
| https://tailscale.com/docs/features/group-visibility-clients | `access-control.md` |
| https://tailscale.com/docs/features/logging | `enterprise.md` |
| https://tailscale.com/docs/features/mac-ios-shortcuts | `installation.md` |
| https://tailscale.com/docs/features/magicdns | `common-tasks.md` |
| https://tailscale.com/docs/features/magicroute | `services-and-routing.md` |
| https://tailscale.com/docs/features/multiple-tailnets | `enterprise.md` |
| https://tailscale.com/docs/features/oauth-apps | `identity-and-credentials.md` |
| https://tailscale.com/docs/features/oauth-clients | `identity-and-credentials.md` |
| https://tailscale.com/docs/features/peer-relay | `connectivity.md` |
| https://tailscale.com/docs/features/route-selection | `services-and-routing.md` |
| https://tailscale.com/docs/features/secure-node-state-storage | `device-management.md` |
| https://tailscale.com/docs/features/services | `sharing-and-publishing.md` |
| https://tailscale.com/docs/features/sharing | `sharing-and-publishing.md` |
| https://tailscale.com/docs/features/site-to-site | `subnet-routers.md` |
| https://tailscale.com/docs/features/subnet-routers | `subnet-routers.md` |
| https://tailscale.com/docs/features/tags | `access-control.md` |
| https://tailscale.com/docs/features/taildrive | `sharing-and-publishing.md` |
| https://tailscale.com/docs/features/taildrop | `sharing-and-publishing.md` |
| https://tailscale.com/docs/features/tailnet-lock | `connectivity.md` |
| https://tailscale.com/docs/features/tailnet-policy-file | `access-control.md` |
| https://tailscale.com/docs/features/tailnets-api | `api.md` |
| https://tailscale.com/docs/features/tailscale-accessbot-jit | `access-control.md` |
| https://tailscale.com/docs/features/tailscale-funnel | `sharing-and-publishing.md` |
| https://tailscale.com/docs/features/tailscale-serve | `sharing-and-publishing.md` |
| https://tailscale.com/docs/features/tailscale-services | `services-and-routing.md` |
| https://tailscale.com/docs/features/tailscale-skill | this plugin's upstream |
| https://tailscale.com/docs/features/tailscale-ssh | `common-tasks.md` |
| https://tailscale.com/docs/features/tailscale-system-policies | `device-management.md` |
| https://tailscale.com/docs/features/tsidp | `identity-and-credentials.md` |
| https://tailscale.com/docs/features/tsnet | `tsnet.md` |
| https://tailscale.com/docs/features/tsrecorder | `session-recording.md` |
| https://tailscale.com/docs/features/user-group-provisioning | `device-management.md` |
| https://tailscale.com/docs/features/visual-editor | `access-control.md` |
| https://tailscale.com/docs/features/webhooks | `api.md` |
| https://tailscale.com/docs/features/workload-identity-federation | `identity-and-credentials.md` |
